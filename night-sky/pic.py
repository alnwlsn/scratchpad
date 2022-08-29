import os
import time

while True:
    os.system('raspistill -t 10 -bm -ex off -ag 12 -ss 6000000 -st -o $(date +"%s").jpg')
    time.sleep(2)
