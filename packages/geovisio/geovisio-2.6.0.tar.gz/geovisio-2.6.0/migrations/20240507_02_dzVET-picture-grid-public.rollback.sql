-- picture_grid_public
-- depends: 20240507_01_eBfqZ-refresh-table

DROP MATERIALIZED VIEW pictures_grid;

CREATE MATERIALIZED VIEW pictures_grid AS
SELECT
    row_number() over () as id,
    count(*) as nb_pictures,
    g.geom
FROM
    ST_SquareGrid(
        0.1,
        ST_SetSRID(ST_EstimatedExtent('pictures', 'geom'), 4326)
    ) AS g
    JOIN pictures AS p ON p.geom && g.geom
GROUP BY g.geom;