# coding: UTF-8
from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import pymysql.cursors
import os
import param

# mysql settings
connection = pymysql.connect(
	host = "localhost",
	user = "ubuntu",
	passwd = "ubuntu",
	db = "sensor_db",
	charset = "utf8")
cursor = connection.cursor()

def createSql( li ):
    if len(li) == 10:
        sql = "INSERT INTO sensor_tb VALUES(\'" + \
        li[0] + "\'," + \
        li[1] + "," + \
        li[2] + ",\'" + \
        li[3] + "\',\'" + \
        li[4] + "\'," + \
        li[5] + "," + \
        li[6] + "," + \
        li[7] + "," + \
        li[8] + "," + \
        li[9] + ")"
    elif len(li) == 16:
        sql = "INSERT INTO solar_tb VALUES(\'" + \
        li[0] + "\'," + \
        li[1] + "," + \
        li[2] + "," + \
        li[3] + "," + \
        li[4] + "," + \
        li[5] + "," + \
        li[6] + "," + \
        li[7] + "," + \
        li[8] + "," + \
        li[9] + "," + \
        li[10] + "," + \
        li[11] + "," + \
        li[12] + "," + \
        li[13] + "," + \
        li[14] + "," + \
        li[15] + ")"
    return sql


class Handle(BaseHTTPRequestHandler):
    def do_GET(self):
#        print(self.headers)
        self.send_response(200)
    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        text = post_body.decode()

        li = post_body.decode().split(",")

        print(li)
        res = cursor.execute( createSql(li) )
        connection.commit()

"""
        response = { 'status' : 123,
                    'msg' : 'POST DATA OK' }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        responseBody = json.dumps(response) +"\n"
        self.wfile.write(responseBody.encode('utf-8'))
"""

httpd = HTTPServer((param.ADDRESS, param.RCV_PORT), Handle)
print("sensor-data receiver started")
httpd.serve_forever()
