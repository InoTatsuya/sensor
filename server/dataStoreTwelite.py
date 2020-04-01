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
        "lq":list[3][3:],
        "ct":str(int(list[4][3:],16)),
        "ed":list[5][3:],
        "id":list[6][3:],
        "ba":list[7][3:],
        "a1":list[8][3:],
        "a2":list[9][3:],
        "te":str(int(list[10][3:])/100),
        "hu":str(int(list[11][3:])/100)
    }
    return d

def log(s):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    f = open("twelite.log","a")
    print(time + "," + s, file=f )
    f.close()

    if( dataAnalyseTwelite.format_check(s) == 0 ):
        d = conv(s)
        if( d["ed"] == "82022F9C" ):
            f = open("F9C.log","w")
            print(time + "," + d["te"] + "," + d["hu"], file=f )
            f.close()
    elif( dataAnalyseTwelite.format_check(s) > 1 ):
        f = open("twelite_error.log","a")
        print(time + "," + s, file=f )
        f.close()



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


def store(s):
    li = s.split(",")
    print(li)
    res = cursor.execute( createSql(li) )
    connection.commit()
