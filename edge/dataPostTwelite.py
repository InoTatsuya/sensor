import serial
import datetime
import os
import param_edge

# シリアル接続
ser = serial.Serial(param_edge.SERIAL_TWE,115200)

while True:
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = ser.readline().decode("utf-8")
    line = "\'" + time + "," + line.rstrip() + "\'"
    os.system("curl -H 'Content-Type:application/json' -d " + line + " http://" + param_edge.ADDRESS + ":" + "8048" +" -so -X POST " )