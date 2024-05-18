from geovisio.web import utils
from importlib import metadata
import re

API_CONFIG = {
    "openapi": "3.1.0",
    "paths": {
        "/api/docs/specs.json": {
            "get": {
                "summary": "The OpenAPI 3 specification for this API",
                "tags": ["Metadata"],
                "responses": {
                    "200": {
                        "description": "JSON file documenting API routes",
                        "content": {"application/json": {"schema": {"$ref": "https://spec.openapis.org/oas/3.0/schema/2021-09-28"}}},
                    }
                },
            }
        },
        "/api/docs/swagger": {
            "get": {
                "summary": "The human-readable API documentation",
                "tags": ["Metadata"],
                "responses": {"200": {"description": "API Swagger", "content": {"text/html": {}}}},
            }
        },
    },
    "components": {
        "securitySchemes": {
            "bearerToken": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
            "cookieAuth": {"type": "apiKey", "in": "cookie", "name": "session"},
        },
        "schemas": {
            "STACLanding": {"$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/core/openapi.yaml#/components/schemas/landingPage"},
            "STACConformance": {"$ref": "http://schemas.opengis.net/ogcapi/features/part1/1.0/openapi/schemas/confClasses.yaml"},
            "STACCatalog": {"$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/core/openapi.yaml#/components/schemas/catalog"},
            "STACCollections": {
                "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/collections/openapi.yaml#/components/schemas/collections"
            },
            "STACCollection": {
                "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/collections/openapi.yaml#/components/schemas/collection"
            },
            "STACCollectionItems": {
                # The following link is the one that should be used, but is broken due to geometryCollectionGeoJSON definition
                # "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/featureCollectionGeoJSON"
                # So using instead copy/pasta version
                "type": "object",
                "required": ["type", "features"],
                "properties": {
                    "type": {"type": "string", "enum": ["FeatureCollection"]},
                    "features": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/STACItem"},
                    },
                    "links": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/links"
                    },
                    "timeStamp": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/timeStamp"
                    },
                    "numberMatched": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/numberMatched"
                    },
                    "numberReturned": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/numberReturned"
                    },
                },
            },
            "STACItem": {
                # The following link is the one that should be used, but is broken due to geometryCollectionGeoJSON definition
                # "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/item"
                # So using instead copy/pasta version
                "type": "object",
                "description": "A GeoJSON Feature augmented with foreign members that contain values relevant to a STAC entity",
                "required": ["stac_version", "id", "type", "geometry", "bbox", "links", "properties", "assets"],
                "properties": {
                    "type": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/itemType"
                    },
                    "geometry": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/pointGeoJSON"
                    },
                    "properties": {"type": "object", "nullable": "true"},
                    "stac_version": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/stac_version"
                    },
                    "stac_extensions": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/stac_extensions"
                    },
                    "id": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/itemId"
                    },
                    "links": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/links"
                    },
                    "properties": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/properties"
                    },
                    "assets": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/assets"
                    },
                },
            },
            "STACExtent": {"$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/collections/openapi.yaml#/components/schemas/extent"},
            "STACExtentTemporal": {
                "type": "object",
                "properties": {
                    "temporal": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/collections/openapi.yaml#/components/schemas/extent/properties/temporal"
                    },
                },
            },
            "STACStatsForItems": {"$ref": "https://stac-extensions.github.io/stats/v0.2.0/schema.json#/definitions/stats_for_items"},
            "STACLinks": {
                "type": "object",
                "properties": {
                    "links": {"$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/collections/openapi.yaml#/components/schemas/links"}
                },
            },
            "STACItemSearchBody": {
                "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/schemas/searchBody"
            },
            "MapLibreStyleJSON": {
                "type": "object",
                "description": """
MapLibre Style JSON, see https://maplibre.org/maplibre-style-spec/ for reference.

Source ID is either \"geovisio\" or \"geovisio_\{userId\}\".

Layers ID are \"geovisio_grid\", \"geovisio_sequences\" and \"geovisio_pictures\", or with user UUID included (\"geovisio_\{userId\}_sequences\" and \"geovisio_\{userId\}_pictures\").

Note that you may not rely only on these ID that could change through time.
""",
                "properties": {
                    "version": {"type": "integer", "example": 8},
                    "name": {"type": "string", "example": "GeoVisio Vector Tiles"},
                    "sources": {
                        "type": "object",
                        "properties": {
                            "geovisio": {
                                "type": "object",
                                "properties": {
                                    "type": {"type": "string", "example": "vector"},
                                    "minzoom": {"type": "integer", "example": "0"},
                                    "maxzoom": {"type": "integer", "example": "15"},
                                    "tiles": {"type": "array", "items": {"type": "string"}},
                                },
                            }
                        },
                    },
                    "layers": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "source": {"type": "string"},
                                "source-layer": {"type": "string"},
                                "type": {"type": "string"},
                                "paint": {"type": "object"},
                                "layout": {"type": "object"},
                            },
                        },
                    },
                },
            },
            "GeoVisioLanding": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACLanding"},
                    {"type": "object", "properties": {"extent": {"$ref": "#/components/schemas/STACExtent"}}},
                ]
            },
            "GeoVisioCatalog": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACCatalog"},
                    {
                        "type": "object",
                        "properties": {
                            "links": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["href", "rel"],
                                    "properties": {
                                        "stats:items": {"$ref": "#/components/schemas/STACStatsForItems"},
                                        "extent": {"$ref": "#/components/schemas/STACExtentTemporal"},
                                        "geovisio:status": {"$ref": "#/components/schemas/GeoVisioCollectionStatus"},
                                    },
                                },
                            }
                        },
                    },
                ]
            },
            "GeoVisioCollectionOfCollection": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACCollection"},
                    {
                        "type": "object",
                        "properties": {
                            "links": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["href", "rel"],
                                    "properties": {
                                        "stats:items": {"$ref": "#/components/schemas/STACStatsForItems"},
                                        "extent": {"$ref": "#/components/schemas/STACExtentTemporal"},
                                        "geovisio:status": {"$ref": "#/components/schemas/GeoVisioCollectionStatus"},
                                        "created": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "Upload date of the collection",
                                        },
                                        "updated": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "Update date of the collection",
                                        },
                                    },
                                },
                            }
                        },
                    },
                ]
            },
            "GeoVisioCollections": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACCollections"},
                    {"$ref": "#/components/schemas/STACLinks"},
                    {
                        "type": "object",
                        "properties": {"collections": {"type": "array", "items": {"$ref": "#/components/schemas/GeoVisioCollection"}}},
                    },
                ]
            },
            "GeoVisioCollectionsRSS": {
                "type": "object",
                "xml": {"name": "rss"},
                "required": ["version", "channel"],
                "properties": {
                    "version": {"type": "string", "example": "2.0", "xml": {"attribute": True}},
                    "channel": {
                        "type": "object",
                        "required": ["title", "link", "description", "generator", "docs"],
                        "properties": {
                            "title": {"type": "string"},
                            "link": {"type": "string", "format": "uri"},
                            "description": {"type": "string"},
                            "language": {"type": "string"},
                            "lastBuildDate": {"type": "string"},
                            "generator": {"type": "string"},
                            "docs": {"type": "string", "format": "uri"},
                            "image": {
                                "type": "object",
                                "properties": {
                                    "url": {"type": "string", "format": "uri"},
                                    "title": {"type": "string"},
                                    "link": {"type": "string", "format": "uri"},
                                },
                            },
                            "item": {"type": "array", "items": {"$ref": "#/components/schemas/GeoVisioItemRSS"}},
                        },
                    },
                },
            },
            "GeoVisioCollection": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACCollection"},
                    {
                        "type": "object",
                        "properties": {
                            "stats:items": {"$ref": "#/components/schemas/STACStatsForItems"},
                            "geovisio:status": {"$ref": "#/components/schemas/GeoVisioCollectionStatus"},
                            "geovisio:sorted-by": {"$ref": "#/components/schemas/GeoVisioCollectionSortedBy"},
                        },
                    },
                ]
            },
            "GeoVisioCollectionImportStatus": {
                "type": "object",
                "properties": {
                    "status": {"$ref": "#/components/schemas/GeoVisioCollectionStatus"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "status": {"$ref": "#/components/schemas/GeoVisioItemStatus"},
                                "processing_in_progress": {"type": "boolean"},
                                "rank": {"type": "integer"},
                                "nb_errors": {"type": "integer"},
                                "process_error": {"type": "string"},
                                "processed_at": {"type": "string", "format": "date-time"},
                            },
                        },
                    },
                },
            },
            "GeoVisioPostCollection": {
                "type": "object",
                "properties": {"title": {"type": "string", "description": "The sequence title"}},
            },
            "GeoVisioPatchCollection": {
                "type": "object",
                "properties": {
                    "visible": {
                        "type": "string",
                        "description": "Should the sequence be publicly visible ?",
                        "enum": ["true", "false", "null"],
                        "default": "null",
                    },
                    "title": {
                        "type": "string",
                        "description": "The sequence title (publicly displayed)",
                    },
                    "relative_heading": {
                        "type": "number",
                        "minimum": -180,
                        "maximum": 180,
                        "description": "The relative heading (in degrees), offset based on movement path (0° = looking forward, -90° = looking left, 90° = looking right). Headings are unchanged if this parameter is not set.",
                    },
                    "sortby": {
                        "description": """
Define the pictures sort order based on given property. Sort order is defined based on preceding '+' (asc) or '-' (desc).

Available properties are:
* `gpsdate`: sort by GPS datetime
* `filedate`: sort by the camera-generated capture date. This is based on EXIF tags `Exif.Image.DateTimeOriginal`, `Exif.Photo.DateTimeOriginal`, `Exif.Image.DateTime` or `Xmp.GPano.SourceImageCreateTime` (in this order).
* `filename`: sort by the original picture file name

If unset, sort order is unchanged.
""",
                        "type": "string",
                        "enum": ["+gpsdate", "-gpsdate", "+filedate", "-filedate", "+filename", "-filename"],
                    },
                },
            },
            "GeoVisioCollectionItems": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACCollectionItems"},
                    {"$ref": "#/components/schemas/STACLinks"},
                    {
                        "type": "object",
                        "properties": {"features": {"type": "array", "items": {"$ref": "#/components/schemas/GeoVisioItem"}}},
                    },
                ]
            },
            "GeoVisioItem": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACItem"},
                    {
                        "type": "object",
                        "properties": {
                            "properties": {
                                "type": "object",
                                "properties": {
                                    "datetimetz": {
                                        "type": "string",
                                        "format": "date-time",
                                        "title": "Date & time with original timezone information",
                                    },
                                    "geovisio:status": {"$ref": "#/components/schemas/GeoVisioItemStatus"},
                                    "geovisio:producer": {"type": "string"},
                                    "geovisio:image": {"type": "string", "format": "uri"},
                                    "geovisio:thumbnail": {"type": "string", "format": "uri"},
                                    "original_file:size": {"type": "integer", "minimum": 0, "title": "Size of the original file, in bytes"},
                                    "original_file:name": {"type": "string", "title": "Original file name"},
                                },
                            }
                        },
                    },
                ],
            },
            "GeoVisioItemRSS": {
                "type": "object",
                "required": ["title", "link", "description", "author", "pubDate", "point"],
                "properties": {
                    "title": {"type": "string"},
                    "link": {"type": "string", "format": "uri"},
                    "description": {"type": "string"},
                    "author": {"type": "string"},
                    "pubDate": {"type": "string"},
                    "enclosure": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "format": "uri", "xml": {"attribute": True}},
                            "length": {"type": "integer", "xml": {"attribute": True}},
                            "type": {"type": "string", "xml": {"attribute": True}},
                        },
                    },
                    "guid": {"type": "string", "format": "uri"},
                    "point": {"type": "string", "xml": {"namespace": "http://www.georss.org/georss", "prefix": "georss"}},
                    "encoded": {"type": "string", "xml": {"namespace": "http://purl.org/rss/1.0/modules/content/", "prefix": "content"}},
                },
            },
            "GeoVisioPostItem": {
                "type": "object",
                "patternProperties": {
                    "override_(Exif|Xmp)\..+": {
                        "type": "string",
                        "description": "An EXIF or XMP tag to use instead of existing one in picture file metadata. The query name can be any valid Exiv2 property name.",
                    }
                },
                "properties": {
                    "position": {"type": "integer", "description": "Position of picture in sequence (starting from 1)"},
                    "picture": {
                        "type": "string",
                        "format": "binary",
                        "description": "Picture to upload",
                    },
                    "isBlurred": {
                        "type": "string",
                        "description": "Is picture blurred",
                        "enum": ["true", "false", "null"],
                        "default": "false",
                    },
                    "override_capture_time": {
                        "type": "string",
                        "format": "date-time",
                        "description": "datetime when the picture was taken. It will change the picture's metadata with this datetime. It should be an iso 3339 formated datetime (like '2017-07-21T17:32:28Z')",
                    },
                    "override_latitude": {
                        "type": "number",
                        "format": "double",
                        "description": "latitude of the picture in decimal degrees (WGS84 / EPSG:4326). It will change the picture's metadata with this latitude.",
                    },
                    "override_longitude": {
                        "type": "number",
                        "format": "double",
                        "description": "longitude of the picture in decimal degrees (WGS84 / EPSG:4326). It will change the picture's metadata with this longitude.",
                    },
                },
            },
            "GeoVisioItemSearchBody": {
                "description": "The search criteria",
                "type": "object",
                "allOf": [
                    {"$ref": "#/components/schemas/STACItemSearchBody"},
                    {
                        "type": "object",
                        "properties": {
                            "place_position": {
                                "description": "Geographical coordinates (lon,lat) of a place you'd like to have pictures of. Returned pictures are either 360° or looking in direction of wanted place.",
                                "type": "string",
                                "pattern": "-?\d+\.\d+,-?\d+\.\d+",
                            },
                            "place_distance": {
                                "description": "Distance range (in meters) to search pictures for a particular place (place_position). Default range is 3-15. Only used if place_position parameter is defined.",
                                "type": "string",
                                "pattern": "\d+-\d+",
                            },
                            "place_fov_tolerance": {
                                "type": "integer",
                                "minimum": 2,
                                "maximum": 180,
                                "description": """
Tolerance on how much the place should be centered in nearby pictures:

 * A lower value means place have to be at the very center of picture
 * A higher value means place could be more in picture sides

Value is expressed in degrees (from 2 to 180, defaults to 30°), and represents the acceptable field of view relative to picture heading. Only used if place_position parameter is defined.

Example values are:

 * <= 30° for place to be in the very center of picture
 * 60° for place to be in recognizable human field of view
 * 180° for place to be anywhere in a wide-angle picture

Note that this parameter is not taken in account for 360° pictures, as by definition a nearby place would be theorically always visible in it.
""",
                            },
                        },
                    },
                ],
            },
            "GeoVisioPatchItem": {
                "type": "object",
                "properties": {
                    "visible": {
                        "type": "string",
                        "description": "Should the picture be publicly visible ?",
                        "enum": ["true", "false", "null"],
                        "default": "null",
                    },
                    "heading": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 360,
                        "description": "The picture heading (in degrees). North is 0°, East = 90°, South = 180° and West = 270°.",
                    },
                },
            },
            "GeoVisioCollectionStatus": {"type": "string", "enum": ["ready", "broken", "preparing", "waiting-for-process"]},
            "GeoVisioCollectionSortedBy": {
                "description": """
Define the pictures sort order of the sequence. Null by default, and can be set via the collection PATCH.
Sort order is defined based on preceding '+' (asc) or '-' (desc).

Available properties are:
* `gpsdate`: sort by GPS datetime
* `filedate`: sort by the camera-generated capture date. This is based on EXIF tags `Exif.Image.DateTimeOriginal`, `Exif.Photo.DateTimeOriginal`, `Exif.Image.DateTime` or `Xmp.GPano.SourceImageCreateTime` (in this order).
* `filename`: sort by the original picture file name
""",
                "type": "string",
                "enum": ["+gpsdate", "-gpsdate", "+filedate", "-filedate", "+filename", "-filename"],
            },
            "GeoVisioItemStatus": {
                "type": "string",
                "enum": ["ready", "broken", "waiting-for-process"],
            },
            "GeoVisioUserList": {
                "type": "object",
                "properties": {
                    "users": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/GeoVisioUser",
                        },
                    },
                },
            },
            "GeoVisioUser": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "format": "uuid"},
                    "name": {"type": "string"},
                    "links": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"href": {"type": "string"}, "ref": {"type": "string"}, "type": {"type": "string"}},
                        },
                    },
                },
            },
            "GeoVisioUserAuth": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "format": "uuid"},
                    "name": {"type": "string"},
                    "oauth_provider": {"type": "string"},
                    "oauth_id": {"type": "string"},
                },
            },
            "GeoVisioUserSearch": {
                "type": "object",
                "properties": {
                    "features": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "label": {"type": "string"},
                                "id": {"type": "string", "format": "uuid"},
                                "links": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {"href": {"type": "string"}, "ref": {"type": "string"}, "type": {"type": "string"}},
                                    },
                                },
                            },
                        },
                    },
                },
            },
            "GeoVisioConfiguration": {
                "type": "object",
                "properties": {
                    "auth": {
                        "type": "object",
                        "properties": {
                            "user_profile": {"type": "object", "properties": {"url": {"type": "string"}}},
                            "enabled": {"type": "boolean"},
                        },
                        "required": ["enabled"],
                    },
                    "license": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "description": "SPDX id of the license"},
                            "url": {"type": "string"},
                        },
                        "required": ["id"],
                    },
                },
                "required": ["auth"],
            },
            "GeoVisioTokens": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "description": {"type": "string"},
                        "generated_at": {"type": "string"},
                        "links": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {"href": {"type": "string"}, "ref": {"type": "string"}, "type": {"type": "string"}},
                            },
                        },
                    },
                },
            },
            "GeoVisioEncodedToken": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "description": {"type": "string"},
                    "generated_at": {"type": "string"},
                    "jwt_token": {
                        "type": "string",
                        "description": "this jwt_token will be needed to authenticate future queries as Bearer token",
                    },
                },
            },
            "JWTokenClaimable": {
                "allOf": [
                    {"$ref": "#/components/schemas/GeoVisioEncodedToken"},
                    {
                        "type": "object",
                        "properties": {
                            "links": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "href": {"type": "string"},
                                        "ref": {"type": "string"},
                                        "type": {"type": "string"},
                                    },
                                },
                            }
                        },
                    },
                ]
            },
        },
        "parameters": {
            "STAC_bbox": {"$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/parameters/bbox"},
            "STAC_intersects": {
                "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/parameters/intersects"
            },
            "STAC_datetime": {
                "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/parameters/datetime"
            },
            "STAC_limit": {"$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/parameters/limit"},
            "STAC_ids": {"$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/parameters/ids"},
            "STAC_collectionsArray": {
                "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/parameters/collectionsArray"
            },
            "STAC_collections_limit": {
                "name": "limit",
                "in": "query",
                "description": "Estimated number of collections that should be present in response. Defaults to 100. Note that response can contain a bit more or a bit less entries due to internal mechanisms.",
                "required": False,
                "schema": {"type": "integer", "minimum": 1, "maximum": 1000},
            },
            "STAC_collections_filter": {
                "name": "filter",
                "in": "query",
                "description": """
A CQL2 filter expression for filtering sequences.

Allowed properties are: 
 * "created": upload date
 * "updated": last edit date
 * "status": status of the sequence. Can either be "ready" (for collections ready to be served) or "deleted"  for deleted collection. By default, only the "ready" collections will be shown.

Usage doc can be found here: https://docs.geoserver.org/2.23.x/en/user/tutorials/cql/cql_tutorial.html

Examples:

* updated >= '2023-12-31'

* updated BETWEEN '2018-01-01' AND '2023-12-31'

* created <= '2023-01-01' AND updated >= '2018-01-01'
""",
                "required": False,
                "schema": {"type": "string"},
            },
            "tiles_filter": {
                "name": "filter",
                "in": "query",
                "description": """
A CQL2 filter expression for filtering tiles.

Allowed properties are: 
 * "status": status of the sequence. Can either be "ready" (for collections ready to be served) or "hidden" for hidden collections. By default, only the "ready" collections will be shown.

Usage doc can be found here: https://docs.geoserver.org/2.23.x/en/user/tutorials/cql/cql_tutorial.html
""",
                "required": False,
                "schema": {"type": "string"},
            },
            "GeoVisio_place_position": {
                "name": "place_position",
                "in": "query",
                "required": False,
                "description": "Geographical coordinates (lon,lat) of a place you'd like to have pictures of. Returned pictures are either 360° or looking in direction of wanted place.",
                "schema": {"type": "string", "pattern": "-?\d+\.\d+,-?\d+\.\d+"},
            },
            "GeoVisio_place_distance": {
                "name": "place_distance",
                "in": "query",
                "required": False,
                "description": "Distance range (in meters) to search pictures for a particular place (place_position). Default range is 3-15. Only used if place_position parameter is defined.",
                "schema": {"type": "string", "pattern": "\d+-\d+", "default": "3-15"},
            },
            "GeoVisio_place_fov_tolerance": {
                "name": "place_fov_tolerance",
                "in": "query",
                "description": """
Tolerance on how much the place should be centered in nearby pictures:

 * A lower value means place have to be at the very center of picture
 * A higher value means place could be more in picture sides

Value is expressed in degrees (from 2 to 180, defaults to 30°), and represents the acceptable field of view relative to picture heading. Only used if place_position parameter is defined.

Example values are:

 * <= 30° for place to be in the very center of picture
 * 60° for place to be in recognizable human field of view
 * 180° for place to be anywhere in a wide-angle picture

Note that this parameter is not taken in account for 360° pictures, as by definition a nearby place would be theorically always visible in it.
""",
                "required": False,
                "schema": {"type": "integer", "minimum": 2, "maximum": 180, "default": 30},
            },
            "OGC_sortby": {
                "name": "sortby",
                "in": "query",
                "required": False,
                "description": """
Define the sort order based on given property. Sort order is defined based on preceding '+' (asc) or '-' (desc).

Available properties are: "created", "updated", "datetime".

Default sort is "-created".
""",
                "schema": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "string",
                        "pattern": "[+|-]?[A-Za-z_].*",
                    },
                },
            },
        },
        "responses": {
            "STAC_search": {
                "description": "the items list",
                "content": {
                    "application/geo+json": {
                        "schema": {
                            "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/schemas/itemCollection"
                        }
                    }
                },
            },
        },
    },
    "specs": [
        {
            "endpoint": "swagger",
            "route": "/api/docs/specs.json",
        }
    ],
    "swagger_ui": True,
    "specs_route": "/api/docs/swagger",
    "swagger_ui_bundle_js": "//unpkg.com/swagger-ui-dist@5.9/swagger-ui-bundle.js",
    "swagger_ui_standalone_preset_js": "//unpkg.com/swagger-ui-dist@5.9/swagger-ui-standalone-preset.js",
    "jquery_js": "//unpkg.com/jquery@2.2.4/dist/jquery.min.js",
    "swagger_ui_css": "//unpkg.com/swagger-ui-dist@5.9/swagger-ui.css",
}
AUTHOR_RGX = re.compile(r"(?P<Name>.*) \<(?P<Email>.*)\>")


def getApiInfo():
    """Return API metadata parsed from pyproject.toml"""
    apiMeta = metadata.metadata("geovisio")

    # url is formated like 'Home, <url>
    url = apiMeta["Project-URL"].split(",")[1].rstrip()
    # there can be several authors, but we only display the first one in docs
    author = apiMeta["Author-email"].split(",")[0]
    m = AUTHOR_RGX.match(author)
    if not m:
        raise Exception("impossible to find email in pyproject")
    name = m.group("Name")
    email = m.group("Email")

    return {
        "title": apiMeta["Name"],
        "version": apiMeta["Version"],
        "description": apiMeta["Description"],
        "contact": {"name": name, "url": url, "email": email},
    }


def getApiDocs():
    """Returns API documentation object for Swagger"""

    return {
        "info": getApiInfo(),
        "tags": [
            {"name": "Metadata", "description": "API metadata"},
            {"name": "Sequences", "description": "Collections of pictures"},
            {"name": "Pictures", "description": "Geolocated images"},
            {"name": "Map", "description": "Tiles for web map display"},
            {"name": "Upload", "description": "Sending pictures & sequences"},
            {"name": "Editing", "description": "Modifying pictures & sequences"},
            {"name": "Users", "description": "Account management"},
            {"name": "Auth", "description": "User authentication"},
        ],
    }
