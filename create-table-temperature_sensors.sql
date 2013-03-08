CREATE TABLE temperature_sensors (
	tsid serial NOT NULL PRIMARY KEY,
	sensor_id text NOT NULL UNIQUE,
	location text NOT NULL,
	location_type text NOT NULL,
	name text NOT NULL
);
