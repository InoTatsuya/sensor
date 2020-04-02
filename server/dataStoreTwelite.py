# coding: UTF-8
from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import pymysql.cursors
import os
import param_server
import dataAnalyseTwelite

# mysql settings
connection = pymysql.connect(
	host = "localhost",
	user = "ubuntu",
	passwd = "ubuntu",
	db = "sensor_db",
	charset = "utf8")
cursor = connection.cursor()

def conv_(s):
    list = s.split(":")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lq = list[3][3:]
    ct = str(int(list[4][3:],16))
    ed = list[5][3:]
    id = list[6][3:]
    ba = list[7][3:]
    a1 = list[8][3:]
    a2 = list[9][3:]
    te = str(int(list[10][3:])/100)
    hu = str(int(list[11][3:])/100)

def conv(s):
    list = s.split(":")
    d = {
        "time":list[0] + ":" + list[1] + ":" + list[2],
        "lq":list[6][3:],
        "ct":str(int(list[7][3:],16)),
        "ed":list[8][3:],
        "id":list[9][3:],
        "ba":list[10][3:],
        "a1":list[11][3:],
        "a2":list[12][3:],
        "te":str(int(list[13][3:])/100),
        "hu":str(int(list[14][3:])/100)
    }
    return d

def log(s):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if( dataAnalyseTwelite.format_check(s) == 0 ):
        f = open("twelite.log","a")
        print(time + ":" + s, file=f )
        f.close()
    elif( dataAnalyseTwelite.format_check(s) > 1 ):
        f = open("twelite_error.log","a")
        print(time + ":" + s, file=f )
        f.close()

def hum_test(s):
    d = conv(s)
    if( d["ed"] == "82025319" ):
        try:
            f = open("F9C.log","a")
            print(d["time"] + "," + d["te"] + "," + d["hu"], file=f )
            f.close()
        except KeyboardInterrupt:
            f.close()

def mysql(s):
    d = conv(s)
    sql = "INSERT INTO sensor_tb VALUES(\'" + \
    d["time"] + "\'," + \
    d["lq"] + "," + \
    d["ct"] + ",\'" + \
    d["ed"] + "\',\'" + \
    d["ba"] + "\'," + \
    d["id"] + "," + \
    d["a1"] + "," + \
    d["a2"] + "," + \
    d["te"] + "," + \
    d["hu"] + ")"
    res = cursor.execute( sql )
    connection.commit()

