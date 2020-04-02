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
            for j in range(row):
                if( liold[j] != liold[i] ):
                    dataStoreTwelite.hum_test(li[i])
                    break
                liold = li[i]
        t2 = time.time()
        print( (t2 - t1).real )
        time.sleep(1)
except KeyboardInterrupt:
    f.close()