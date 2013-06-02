#!/usr/bin/python

import matplotlib, psycopg2
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import dates

db = psycopg2.connect(host='localhost', database='jessebishop',user='jessebishop')
cursor = db.cursor()

#cursor.execute("""SELECT DISTINCT(sensor_id) FROM temperature_measurements;""")
cursor.execute("""SELECT DISTINCT(device_id) FROM temperature_test;""")

sensors = [this[0] for this in cursor.fetchall()]

for sensor in sensors:
	#cursor.execute("""SELECT name FROM temperature_sensors WHERE sensor_id = '%s';""" % sensor)
	#sensorname = cursor.fetchone()[0]
	sensorname = 'testing'
	print sensor
	cursor.execute("""SELECT read_time, temperature * 9 / 5 + 32 AS temp FROM temperature_test WHERE device_id = '%s' AND read_time = CURRENT_TIMESTAMP - (7 * interval '1 day') ORDER BY id;""" % sensor)
	data = cursor.fetchall()
	if not data:
		continue
	timestamp, temperature = zip(*data)
	dts = dates.date2num(timestamp)
	hfmt = dates.DateFormatter('%Y-%m-%d %H:%M:%S')
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(dts,temperature)
	ax.xaxis.set_major_locator(dates.MinuteLocator())
	ax.xaxis.set_major_formatter(hfmt)
	#ax.set_ylim(bottom = min(temperature) - 1)
	#plt.show()

	#plt.plot(dts,temperature)
	#plt.xlim(min(dates), max(dates))

	plt.grid()
	plt.savefig('/var/www/electricity/' + sensor + '.png')



cursor.close()
db.close()



