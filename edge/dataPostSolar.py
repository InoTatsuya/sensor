from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time
import datetime
import os
import json

id = 1

f = open( "config_rasp.json", "r" )
tmp = json.loads( f.read() )
f.close()
ADDR = tmp[ "address" ]

client = ModbusClient(method = 'rtu', port = '/dev/ttyUSB1', baudrate = 115200)

def solarInfoGet():
    client.connect()

    result = client.read_input_registers(0x3100,18,unit=1)
    solarVoltage = float( result.registers[0] / 100.0 )
    solarCurrent = float( result.registers[1] / 100.0 )
    solarPower = float( ( result.registers[3] /100.0 ) + ( result.registers[2] / 100.0 ) )
    batteryVoltage = float( result.registers[4] / 100.0 )
    batteryCurrent = float( result.registers[5] / 100.0 )
    batteryPower = float( ( result.registers[7] / 100.0 ) + ( result.registers[6] / 100.0 ) )
    loadVoltage = float( result.registers[12] / 100.0 )
    loadCurrent = float( result.registers[13] / 100.0 )
    loadPower = float( ( result.registers[15] / 100.0 ) + ( result.registers[14] / 100.0 ) )
    batteryTemp = float( result.registers[16] / 100.0 )
    deviceTemp = float( result.registers[17] / 100.0 )

    time.sleep(0.2)
    result = client.read_input_registers(0x311A,1,unit=1)
    batterySOC = float( result.registers[0] / 100.0 )

    time.sleep(0.2)
    result = client.read_input_registers(0x3200,2,unit=1)
    batteryStatus = result.registers[0]
    chargeStatus = result.registers[1]

    client.close()

    li = [
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        solarCurrent,
        solarVoltage,
        solarPower,
        batteryVoltage,
        batteryCurrent,
        batteryPower,
        batteryTemp,
        batterySOC,
        batteryStatus,
        loadVoltage,
        loadCurrent,
        loadPower,
        deviceTemp,
        chargeStatus,
        id
    ]

    return li


while True:
    data = ",".join( map( str, solarInfoGet() ) )

    print(data)
    var = os.system("curl -H 'Content-Type:application/json' -d \"" + data + "\" http://" + ADDR + ":8049 -so -X POST " )
    print(var)

    time.sleep(10)
