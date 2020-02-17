import serial
import datetime
import os

# シリアル接続
ser = serial.Serial("/dev/ttyUSB3",9600)

# sensorhub settings

while True:
    text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "," + ser.readline().decode().replace("\r\n","")
    f = open( "./sht30.log", "a" )
    print(text, file=f)
    f.close()
