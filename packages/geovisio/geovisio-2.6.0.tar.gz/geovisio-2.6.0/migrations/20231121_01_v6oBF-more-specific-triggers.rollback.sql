-- more specific triggers
-- depends: 20231110_01_3p070-jobs-error

-- put old version of the triggers

DROP FUNCTION IF EXISTS pictures_update_sequence CASCADE;
CREATE FUNCTION pictures_update_sequence() RETURNS trigger AS $$
BEGIN
	UPDATE sequences
	SET geom = s.geom
	FROM (
		SELECT seq_id, ST_MakeLine(array_agg(geom)) AS geom
		FROM (
			SELECT sp.seq_id, sp.rank, p.geom
			FROM sequences_pictures sp
			JOIN pictures p ON sp.pic_id = p.id
			WHERE sp.seq_id IN (
				SELECT DISTINCT sequences_pictures.seq_id
				FROM old_table
				JOIN new_table USING (id)
				JOIN sequences_pictures ON sequences_pictures.pic_id = new_table.id
				WHERE new_table.status != old_table.status OR NOT ST_Equals(old_table.geom, new_table.geom)
			)
			ORDER BY sp.seq_id, sp.rank
		) sp
		GROUP BY seq_id
	) s
	WHERE sequences.id = s.seq_id;
	RETURN NULL;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER pictures_update_sequences_trg
AFTER UPDATE ON pictures
REFERENCING OLD TABLE AS old_table NEW TABLE AS new_table
FOR EACH STATEMENT EXECUTE FUNCTION pictures_update_sequence();

