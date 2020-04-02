import subprocess
import time
import dataStoreTwelite

# define
row = 10

f = open("twelite.log", "r")

liold = subprocess.run(["tail","-n",str(row),"twelite.log"],stdout = subprocess.PIPE, stderr = subprocess.PIPE).stdout.decode("utf8").strip().split("\n")
try:
    while True:
        t1 = time.time()
        li = subprocess.run(["tail","-n",str(row),"twelite.log"],stdout = subprocess.PIPE, stderr = subprocess.PIPE).stdout.decode("utf8").strip().split("\n")
        for i in range(row):
            if( not li[i] in liold ):
                dataStoreTwelite.hum_test(li[i])
                dataStoreTwelite.mysql(li[i])
        liold = li
        t2 = time.time()
        time.sleep(1)
except KeyboardInterrupt:
    f.close()