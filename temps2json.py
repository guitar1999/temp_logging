#!/usr/bin/python

import datetime
import psycopg2
import json
import collections

outfile = '/home/jessebishop/scripts/temp_logging/temps.json'

db = psycopg2.connect(host='localhost', database='jessebishop',user='jessebishop')
cursor = db.cursor()

query = """SELECT read_time, temperature, device_id FROM temperature_test ORDER BY read_time LIMIT 4;"""

cursor.execute(query)
data = cursor.fetchall()

outobject = []
for row in data:
    d = collections.OrderedDict()
    d['read_time'] = datetime.datetime.strftime(row[0], '%Y-%m-%d %H:%M:%S')
    d['temperature'] = float(row[1])
    d['id'] = row[2]
    outobject.append(d)

j = json.dumps(outobject)
f = open(outfile, 'w')
f.write(j)
f.close()


cursor.close()
db.close()

