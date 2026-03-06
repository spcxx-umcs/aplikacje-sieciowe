#!/usr/bin/env python

import socket
import sys

if len(sys.argv) != 2:
    print("Usage: python3 5.py <hostname>")
    sys.exit(1)

user_hostname = sys.argv[1]

try:
    ip = socket.gethostbyname(user_hostname)
    if ip:
        print("IP:", ip)
    else:
        print("Error while getting IP")
except socket.gaierror:
    print("Error while getting IP")