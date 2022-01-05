#!/usr/bin/env python3

import os

def start_listener():
    try:
        os.system('/usr/bin/touch exfil.log; /usr/bin/python3 -m http.server 1337 2> ./exfil.log')
    except KeyboardInterrupt:
        print('Exiting')