import psycopg
from flask import current_app, url_for
from psycopg.types.json import Jsonb
from psycopg import sql
from psycopg.sql import SQL
from psycopg.rows import dict_row
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
import datetime
from uuid import UUID
from enum import Enum
from geovisio.utils.fields import FieldMapping, SortBy, SQLDirection, BBox, Bounds
from geopic_tag_reader import reader
from pathlib import PurePath
from geovisio import errors, utils
import logging
import sentry_sdk


def createSequence(metadata, accountId) -> str:
    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            # Add sequence in database
            seqId = cursor.execute(
                "INSERT INTO sequences(account_id, metadata) VALUES(%s, %s) RETURNING id", [accountId, Jsonb(metadata)]
            ).fetchone()

            # Make changes definitive in database
            conn.commit()

            if seqId is None:
                raise Exception(f"impossible to insert sequence in database")
            return seqId[0]


# Mappings from stac name to SQL names
STAC_FIELD_MAPPINGS = {
    p.stac: p
    for p in [
        FieldMapping(sql_column=sql.SQL("inserted_at"), stac="created"),
        FieldMapping(sql_column=sql.SQL("updated_at"), stac="updated"),
        FieldMapping(sql_column=sql.SQL("computed_capture_date"), stac="datetime"),
        FieldMapping(sql_column=sql.SQL("status"), stac="status"),
    ]
}
STAC_FIELD_TO_SQL_FILTER = {p.stac: p.sql_filter.as_string(None) for p in STAC_FIELD_MAPPINGS.values()}


@dataclass
class Collections:
    """
    Collections as queried from the database
    """

    collections: List[Dict[Any, Any]] = field(default_factory=lambda: [])
    # Bounds of the field used by the first field of the `ORDER BY` (usefull especially for pagination)
    query_first_order_bounds: Optional[Bounds] = None


@dataclass
class CollectionsRequest:
    sort_by: SortBy
    min_dt: Optional[datetime.datetime] = None
    max_dt: Optional[datetime.datetime] = None
    created_after: Optional[datetime.datetime] = None
    created_before: Optional[datetime.datetime] = None
    user_id: Optional[UUID] = None
    bbox: Optional[BBox] = None
    user_filter: Optional[sql.SQL] = None
    pagination_filter: Optional[sql.SQL] = None
    limit: int = 100
    userOwnsAllCollections: bool = False  # bool to represent that the user's asking for the collections is the owner of them

    def filters(self):
        return [f for f in (self.user_filter, self.pagination_filter) if f is not None]


def get_collections(request: CollectionsRequest) -> Collections:
    # Check basic parameters
    seq_filter: List[sql.Composable] = []
    seq_params: dict = {}
    pic_filter = [SQL("sp.seq_id = s.id")]

    # Sort-by parameter
    # Note for review: I'm not sure I understand this non nullity constraint, but if so, shouldn't all sortby fields be added ?
    # for s in request.sort_by.fields:
    #     sqlConditionsSequences.append(SQL("{field} IS NOT NULL").format(field=s.field.sql_filter))
    seq_filter.append(SQL("{field} IS NOT NULL").format(field=request.sort_by.fields[0].field.sql_filter))
    seq_filter.extend(request.filters())

    if request.user_id is not None:
        seq_filter.append(SQL("s.account_id = %(account)s"))
        seq_params["account"] = request.user_id

    if request.user_filter is None or "status" not in request.user_filter.as_string(None):
        # if the filter does not contains any `status` condition, we want to show only 'ready' collection to the general users, and non deleted one for the owner
        if not request.userOwnsAllCollections:
            seq_filter.append(SQL("s.status = 'ready'"))
            pic_filter.append(SQL("p.status = 'ready'"))
        else:
            seq_filter.append(SQL("s.status != 'deleted'"))
    else:
        # else, even if there are status filter, we make sure not to show hidden pictures/sequence to non owner
        if not request.userOwnsAllCollections:
            seq_filter.append(SQL("s.status <> 'hidden'"))
            pic_filter.append(SQL("p.status <> 'hidden'"))

    status_field = None
    if request.userOwnsAllCollections:
        # only logged users can see detailed status
        status_field = SQL("s.status AS status")
    else:
        status_field = SQL("CASE WHEN s.status = 'deleted' THEN s.status ELSE NULL END AS status")

    # Datetime
    if request.min_dt is not None:
        seq_filter.append(SQL("s.computed_capture_date >= %(cmindate)s::date"))
        seq_params["cmindate"] = request.min_dt
    if request.max_dt is not None:
        seq_filter.append(SQL("s.computed_capture_date <= %(cmaxdate)s::date"))
        seq_params["cmaxdate"] = request.max_dt

    if request.bbox is not None:
        seq_filter.append(SQL("ST_Intersects(s.geom, ST_MakeEnvelope(%(minx)s, %(miny)s, %(maxx)s, %(maxy)s, 4326))"))
        seq_params["minx"] = request.bbox.minx
        seq_params["miny"] = request.bbox.miny
        seq_params["maxx"] = request.bbox.maxx
        seq_params["maxy"] = request.bbox.maxy

    # Created after/before
    if request.created_after is not None:
        seq_filter.append(SQL("s.inserted_at > %(created_after)s::timestamp with time zone"))
        seq_params["created_after"] = request.created_after

    if request.created_before:
        seq_filter.append(SQL("s.inserted_at < %(created_before)s::timestamp with time zone"))
        seq_params["created_before"] = request.created_before

    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            sqlSequencesRaw = SQL(
                """
                SELECT
                    s.id,
                    s.status,
                    s.metadata->>'title' AS name,
                    s.inserted_at AS created,
                    s.updated_at AS updated,
                    ST_XMin(s.bbox) AS minx,
                    ST_YMin(s.bbox) AS miny,
                    ST_XMax(s.bbox) AS maxx,
                    ST_YMax(s.bbox) AS maxy,
                    accounts.name AS account_name,
                    ST_X(ST_PointN(s.geom, 1)) AS x1,
                    ST_Y(ST_PointN(s.geom, 1)) AS y1,
                    s.min_picture_ts AS mints,
                    s.max_picture_ts AS maxts,
                    s.nb_pictures AS nbpic,
                    {status},
                    s.computed_capture_date AS datetime
                FROM sequences s
                LEFT JOIN accounts on s.account_id = accounts.id
                WHERE {filter}
                ORDER BY {order1}
                LIMIT {limit}
            """
            )
            sqlSequences = sqlSequencesRaw.format(
                filter=SQL(" AND ").join(seq_filter),
                order1=request.sort_by.as_sql(),
                limit=request.limit,
                pic_filter=SQL(" AND ").join(pic_filter),
                status=status_field,
            )

            # Different request if we want the last n sequences
            #  Useful for paginating from last page to first
            if request.pagination_filter and (
                (
                    request.sort_by.fields[0].direction == SQLDirection.ASC
                    and request.pagination_filter.as_string(None).startswith(
                        f"({request.sort_by.fields[0].field.sql_filter.as_string(None)} <"
                    )
                )
                or (
                    request.sort_by.fields[0].direction == SQLDirection.DESC
                    and request.pagination_filter.as_string(None).startswith(
                        f"({request.sort_by.fields[0].field.sql_filter.as_string(None)} >"
                    )
                )
            ):
                base_query = sqlSequencesRaw.format(
                    filter=SQL(" AND ").join(seq_filter),
                    order1=request.sort_by.revert(),
                    limit=request.limit,
                    pic_filter=SQL(" AND ").join(pic_filter),
                    status=status_field,
                )
                sqlSequences = SQL(
                    """
                    SELECT *
                    FROM ({base_query}) s
                    ORDER BY {order2}
                """
                ).format(
                    order2=request.sort_by.as_sql(),
                    base_query=base_query,
                )

            records = cursor.execute(sqlSequences, seq_params).fetchall()

            query_bounds = None
            for s in records:
                first_order_val = s.get(request.sort_by.fields[0].field.stac)
                if first_order_val is None:
                    continue
                if query_bounds is None:
                    query_bounds = Bounds(first_order_val, first_order_val)
                else:
                    query_bounds.update(first_order_val)

            return Collections(
                collections=records,
                query_first_order_bounds=query_bounds,
            )


def get_pagination_links(
    route: str,
    routeArgs: dict,
    field: str,
    direction: SQLDirection,
    datasetBounds: Bounds,
    dataBounds: Optional[Bounds],
    additional_filters: Optional[str],
) -> List:
    """Computes STAC links to handle pagination"""

    sortby = f"{'+' if direction == SQLDirection.ASC else '-'}{field}"
    links = []
    if dataBounds is None:
        return links

    # Check if first/prev links are necessary
    if (direction == SQLDirection.ASC and datasetBounds.min < dataBounds.min) or (
        direction == SQLDirection.DESC and dataBounds.max < datasetBounds.max
    ):
        links.append(
            {
                "rel": "first",
                "type": "application/json",
                "href": url_for(route, _external=True, **routeArgs, filter=additional_filters, sortby=sortby),
            }
        )
        page_filter = f"{field} {'<' if direction == SQLDirection.ASC else '>'} '{dataBounds.min if direction == SQLDirection.ASC else dataBounds.max}'"
        links.append(
            {
                "rel": "prev",
                "type": "application/json",
                "href": url_for(
                    route,
                    _external=True,
                    **routeArgs,
                    sortby=sortby,
                    filter=additional_filters,
                    page=page_filter,
                ),
            }
        )

    # Check if next/last links are required
    if (direction == SQLDirection.ASC and dataBounds.max < datasetBounds.max) or (
        direction == SQLDirection.DESC and datasetBounds.min < dataBounds.min
    ):
        next_filter = f"{field} {'>' if direction == SQLDirection.ASC else '<'} '{dataBounds.max if direction == SQLDirection.ASC else dataBounds.min}'"
        last_filter = f"{field} {'<=' if direction == SQLDirection.ASC else '>='} '{datasetBounds.max if direction == SQLDirection.ASC else datasetBounds.min}'"
        links.append(
            {
                "rel": "next",
                "type": "application/json",
                "href": url_for(
                    route,
                    _external=True,
                    **routeArgs,
                    sortby=sortby,
                    filter=additional_filters,
                    page=next_filter,
                ),
            }
        )
        links.append(
            {
                "rel": "last",
                "type": "application/json",
                "href": url_for(
                    route,
                    _external=True,
                    **routeArgs,
                    sortby=sortby,
                    filter=additional_filters,
                    page=last_filter,
                ),
            }
        )

    return links


class Direction(Enum):
    """Represent the sort direction"""

    ASC = "+"
    DESC = "-"

    def is_reverse(self):
        return self == Direction.DESC


class CollectionSortOrder(Enum):
    """Represent the sort order"""

    FILE_DATE = "filedate"
    FILE_NAME = "filename"
    GPS_DATE = "gpsdate"


@dataclass
class CollectionSort:
    order: CollectionSortOrder
    direction: Direction

    def as_str(self) -> str:
        return f"{self.direction.value}{self.order.value}"


def sort_collection(db, collectionId: UUID, sortby: CollectionSort):
    """
    Sort a collection by a given parameter

    Note: the transaction is not commited at the end, you need to commit it or use an autocommit connection
    """

    # Remove existing order, and keep list of pictures IDs
    picIds = db.execute(
        SQL(
            """
            DELETE FROM sequences_pictures
            WHERE seq_id = %(id)s
            RETURNING pic_id
            """
        ),
        {"id": collectionId},
    ).fetchall()
    picIds = [p["pic_id"] for p in picIds]

    # Fetch metadata and EXIF tags of concerned pictures
    picMetas = db.execute(SQL("SELECT id, metadata, exif FROM pictures WHERE id = ANY(%s)"), [picIds]).fetchall()
    usedDateField = None
    isFileNameNumeric = False

    if sortby.order == CollectionSortOrder.FILE_NAME:
        # Check if filenames are numeric
        try:
            for pm in picMetas:
                int(PurePath(pm["metadata"]["originalFileName"] or "").stem)
            isFileNameNumeric = True
        except ValueError:
            pass

    if sortby.order == CollectionSortOrder.FILE_DATE:
        # Look out what EXIF field is used for storing dates in this sequence
        for field in [
            "Exif.Image.DateTimeOriginal",
            "Exif.Photo.DateTimeOriginal",
            "Exif.Image.DateTime",
            "Xmp.GPano.SourceImageCreateTime",
        ]:
            if field in picMetas[0]["exif"]:
                usedDateField = field
                break

        if usedDateField is None:
            raise errors.InvalidAPIUsage(
                "Sort by file date is not possible on this sequence (no file date information available on pictures)",
                status_code=422,
            )

    for pm in picMetas:
        # Find value for wanted sort
        if sortby.order == CollectionSortOrder.GPS_DATE:
            pm["sort"] = reader.decodeGPSDateTime(pm["exif"], "Exif.GPSInfo")[0]
        elif sortby.order == CollectionSortOrder.FILE_DATE:
            assert usedDateField  # nullity has been checked before
            pm["sort"] = reader.decodeDateTimeOriginal(pm["exif"], usedDateField)[0]
        elif sortby.order == CollectionSortOrder.FILE_NAME:
            pm["sort"] = pm["metadata"].get("originalFileName")
            if isFileNameNumeric:
                pm["sort"] = int(PurePath(pm["sort"]).stem)

        # Fail if sort value is missing
        if pm["sort"] is None:
            raise errors.InvalidAPIUsage(
                f"Sort using {sortby} is not possible on this sequence, picture {pm['id']} is missing mandatory metadata",
                status_code=422,
            )

    # Actual sorting of pictures
    picMetas.sort(key=lambda p: p["sort"], reverse=sortby.direction.is_reverse())
    picForDb = [(collectionId, i + 1, p["id"]) for i, p in enumerate(picMetas)]

    # Inject back pictures in sequence
    db.executemany(
        SQL(
            """
            INSERT INTO sequences_pictures(seq_id, rank, pic_id)
            VALUES (%s, %s, %s)
            """
        ),
        picForDb,
    )


def update_headings(
    db,
    sequenceId: UUID,
    editingAccount: Optional[UUID] = None,
    relativeHeading: int = 0,
    updateOnlyMissing: bool = True,
):
    """Defines pictures heading according to sequence path.
    Database is not committed in this function, to make entry definitively stored
    you have to call db.commit() after or use an autocommit connection.

    Parameters
    ----------
    db : psycopg.Connection
            Database connection
    sequenceId : uuid
            The sequence's uuid, as stored in the database
    relativeHeading : int
            Camera relative orientation compared to path, in degrees clockwise.
            Example: 0° = looking forward, 90° = looking to right, 180° = looking backward, -90° = looking left.
    updateOnlyMissing : bool
            If true, doesn't change existing heading values in database
    """

    db.execute(
        SQL(
            """
		WITH h AS (
			SELECT
				p.id,
                p.heading AS old_heading,
				CASE
					WHEN LEAD(sp.rank) OVER othpics IS NULL AND LAG(sp.rank) OVER othpics IS NULL
						THEN NULL
					WHEN LEAD(sp.rank) OVER othpics IS NULL
						THEN (360 + FLOOR(DEGREES(ST_Azimuth(LAG(p.geom) OVER othpics, p.geom)))::int + (%(diff)s %% 360)) %% 360
					ELSE
						(360 + FLOOR(DEGREES(ST_Azimuth(p.geom, LEAD(p.geom) OVER othpics)))::int + (%(diff)s %% 360)) %% 360
				END AS heading
			FROM pictures p
			JOIN sequences_pictures sp ON sp.pic_id = p.id AND sp.seq_id = %(seq)s
			WINDOW othpics AS (ORDER BY sp.rank)
		) 
		UPDATE pictures p
		SET heading = h.heading, heading_computed = true {editing_account}
		FROM h
		WHERE h.id = p.id {update_missing}
		"""
        ).format(
            update_missing=SQL(" AND (p.heading IS NULL OR p.heading = 0 OR p.heading_computed)") if updateOnlyMissing else SQL(""),
            editing_account=SQL(", last_account_to_edit = %(account)s") if editingAccount is not None else SQL(""),
        ),  # lots of camera have heading set to 0 for unset heading, so we recompute the heading when it's 0 too, even if this could be a valid value
        {"seq": sequenceId, "diff": relativeHeading, "account": editingAccount},
    )


def update_pictures_grid(db) -> bool:
    """Refreshes the pictures_grid materialized view for an up-to-date view of pictures availability on map.

    Note: the transaction is not commited at the end, you need to commit it or use an autocommit connection.

    Parameters
    ----------
    db : psycopg.Connection
            Database connection

    Returns
    -------
    bool : True if the view has been updated else False
    """
    logger = logging.getLogger("geovisio.picture_grid")
    with db.transaction():
        try:
            db.execute("SELECT refreshed_at FROM refresh_database FOR UPDATE NOWAIT").fetchone()
        except psycopg.errors.LockNotAvailable:
            logger.info("Database refresh already in progress, nothing to do")
            return False

        with sentry_sdk.start_span(description="Refreshing database") as span:
            with utils.time.log_elapsed(f"Refreshing database", logger=logger):
                logger.info("Refreshing database")
                db.execute("UPDATE refresh_database SET refreshed_at = NOW()")
                db.execute("REFRESH MATERIALIZED VIEW pictures_grid")
    return True
