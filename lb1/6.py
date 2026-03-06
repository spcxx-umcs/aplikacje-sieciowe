#!/usr/bin/env python

import socket
import sys
import re

if len(sys.argv) != 3:
    print("Usage: python3 6.py <server ip / hostname> <server port>")
    sys.exit(1)

server_host = sys.argv[1]
try:
    server_port = int(sys.argv[2])
except ValueError:
    print("Invalid port number")
    sys.exit(1)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((server_host, server_port))

    print("Connection established successfully")

    s.close()
except socket.timeout:
    print("Connection timed out")
except Exception:
    print("Connection failed")
