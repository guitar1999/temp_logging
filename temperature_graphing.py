#!/bin/env python

import psycopg2
import matplotlib.pyplot as plt

db = psycopg2.connect(host='localhost', database='jessebishop',user='jessebishop')
cursor = db.cursor()

#cursor.execute("""SELECT DISTINCT(sensor_id) FROM temperature_measurements;""")
cursor.execute("""SELECT DISTINCT(device_id) FROM temperature_test;""")

sensors = [this[0] for this in cursor.fetchall()]

for sensor in sensors:
	#cursor.execute("""SELECT name FROM temperature_sensors WHERE sensor_id = '%s';""" % sensor)
	#sensorname = cursor.fetchone()[0]
	sensorname = 'testing'
	#cursor.execute("""SELECT measurement_time, temperature * 9 / 5 + 32 AS temp FROM temperature_measurement WHERE sensor_id = '%s';""" % sensor)
	cursor.execute("""SELECT read_time, temperature * 9 / 5 + 32 AS temp FROM temperature_test WHERE device_id = '%s';""" % sensor)
	data = cursor.fetchall()
	timestamp, temperature = zip(*data)



cursor.close()
db.close()



