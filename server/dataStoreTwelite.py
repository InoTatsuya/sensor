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

def write(filename, text):
    file_path = os.path.dirname(filename)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(filename, 'a') as f:
        f.write(text + "\n")

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
    list = s.split(",")[1].split(":")
    list.insert(0,s.split(",")[0])
    d = {
        "time":list[0],
        "lq":list[4][3:],
        "ct":str(int(list[5][3:],16)),
        "ed":list[6][3:],
        "id":list[7][3:],
        "ba":list[8][3:],
        "a1":list[9][3:],
        "a2":list[10][3:],
        "te":str(int(list[11][3:])/100),
        "hu":str(int(list[12][3:])/100)
    }
    return d

def log(s):
    dirname = "./log"
    path = datetime.datetime.now().strftime("/%Y/%m/%d/")
    filename = datetime.datetime.now().strftime("%H") + ".txt"
    write(dirname + path + filename, s)
    if( dataAnalyseTwelite.format_check(s) == 0 ):
        write(dirname + "/twelite.log",s)
    elif( dataAnalyseTwelite.format_check(s) > 1 ):
        write(dirname + "/twelite_error.log",s)

def hum_test(s):
    d = conv(s)
    if( d["ed"] == "82025319" ):
        try:
            f = open("F9C.log","w")
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

