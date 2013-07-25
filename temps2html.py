#!/usr/bin/python

import datetime
import psycopg2
import json
import collections

outfile = '/home/jessebishop/scripts/temp_logging/temps.html'
f = open(outfile, 'w')

headhtml = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>TEMPERATURE</title>
  <script type="text/javascript" src="jquery-1.6.2.min.js"></script>
  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript">
    google.load('visualization', '1', {packages: ['annotatedtimeline']});
    function drawVisualization() {
        var data = new google.visualization.DataTable();
        data.addColumn('date', 'Read Time');
        data.addColumn('number', 'Temperature');
        data.addColumn('string', 'Device ID');
        data.addRows([
"""
tailhtml = """        ]);
      var annotatedtimeline = new google.visualization.AnnotatedTimeLine(
          document.getElementById('visualization'));
      annotatedtimeline.draw(data, {'displayAnnotations': false});
    }
    
    google.setOnLoadCallback(drawVisualization);

  </script>
</head>
<body style="font-family: Arial;border: 0 none;">
<div id="visualization" style="width: 800px; height: 400px;"></div>
</body>
</html>
"""

f.write(headhtml)


db = psycopg2.connect(host='localhost', database='jessebishop',user='jessebishop')
cursor = db.cursor()

query = """SELECT date_part('year', read_time) AS year, date_part('month', read_time) AS month, date_part('day', read_time) AS day, date_part('hour', read_time) AS hour, date_part('minute', read_time) AS minute, date_part('second', read_time) AS second, temperature * 9.0 / 5 + 32 AS temperature, device_id FROM temperature_test ORDER BY read_time desc LIMIT 200000;"""

cursor.execute(query)
data = cursor.fetchall()
cursor.close()
db.close()

i = 0
for row in data:
    i += 1
    outstring = """            [new Date(%s,%s,%s,%s,%s,%s), %s, "%s"]""" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
    if i < len(data):
        outstring = outstring + ",\n"
    else:
        outstring = outstring + "\n"
    f.write(outstring)

f.write(tailhtml)
f.close()
    


