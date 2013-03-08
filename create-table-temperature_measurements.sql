CREATE TABLE temperature_measurements (
	tmid serial NOT NULL PRIMARY KEY,
	sensor_id text NOT NULL REFERENCES temperature_sensors (sensor_id),
	temperature numeric NOT NULL,
	measurement_time timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
