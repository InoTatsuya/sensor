import serial
import datetime
import os
import json

# シリアル接続
ser = serial.Serial("/dev/ttyUSB0",115200)

# sensorhub settings
f = open( "config_rasp.json", "r" )
tmp = json.loads( f.read() )
f.close()
ADDR = tmp[ "address" ]

def format_conv( st ):
    list = st.split(":")
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
    data = "\'"+time+"\',"+lq+","+ct+",\'"+ed+"\',\'"+id+"\',"+ba+","+a1+","+a2+","+te+","+hu
    print(data)
    os.system("curl -H 'Content-Type:application/json' -d " + data + " http://" + ADDR + ":8049 -so -X POST " )

while True:
    line = ser.readline().decode("utf-8")
    if -1 != line.find("rc"):
        format_conv( line )

