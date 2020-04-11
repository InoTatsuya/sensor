import subprocess
import time
import dataStoreTwelite
import datetime
import dataAnalyseTwelite
import os

# define
row = 10

filename = datetime.datetime.now().strftime("log/%Y/%m/%d/%H.txt")
liold = subprocess.run(["tail","-n",str(row),filename],stdout = subprocess.PIPE, stderr = subprocess.PIPE).stdout.decode("utf8").strip().split("\n")
try:
    while True:
        filename = datetime.datetime.now().strftime("log/%Y/%m/%d/%H.txt")
        li = subprocess.run(["tail","-n",str(row), filename],stdout = subprocess.PIPE, stderr = subprocess.PIPE).stdout.decode("utf8").strip().split("\n")
        res = os.path.isfile(filename)
        if( res and ( len(li[0]) != "" ) ):
            for i in range(len(li)):
                if( not li[i] in liold ):
                    if( dataAnalyseTwelite.format_check(li[i]) == 0 ):
                        dataStoreTwelite.hum_test(li[i])
                        dataStoreTwelite.mysql(li[i])

        liold = li
        time.sleep(1)
except KeyboardInterrupt:
    print("close\n")
