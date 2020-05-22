import serial
import datetime
import subprocess as sp
import param_edge

# シリアル接続
ser = serial.Serial(param_edge.SERIAL_TWE,115200)

while True:
    line = ser.readline().decode("utf-8").replace("\0","").replace("\n","")
    print(line.encode())
    if line:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = "\'" + time + "," + line.rstrip() + "\'"
        line = "curl -H 'Content-Type:application/json' -d " + line + " http://" + param_edge.ADDRESS + ":" + "8049" +" -so -X POST "
        print(line.encode())
        sp.Popen(line, shell=True)
#        print("send!")
    else:
        print( "line is b'0x00'!!!" )
