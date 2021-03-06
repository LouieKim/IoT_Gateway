import os
import signal
import subprocess
import time
import psutil

def main():
    while True:
        #pidResult = subprocess.call("pgrep -x eccSimul", shell=True)
        pid_check = "supervisord" in (p.name() for p in psutil.process_iter())

        if pid_check == True:
            print("eccServer running")
        else:
            print("eccServer not")
            subprocess.call("supervisord -c /home/pi/ecc_pjt_v02/supervisord.conf", shell=True)
            #proc = subprocess.Popen("supervisord -c /etc/supervisord.conf")
            #print(proc.pid)
        time.sleep(10)

if __name__ == "__main__":
    main()