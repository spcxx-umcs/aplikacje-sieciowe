#!/usr/bin/env python

import socket
import re
import sys

if len(sys.argv) != 2:
    print("Usage: python3 4.py <ip>")
    sys.exit(1)

user_ip = sys.argv[1]

valid = re.search( r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", user_ip)
if valid:
    try:
        hostname, _, _ = socket.gethostbyaddr(user_ip)
        if hostname:
            print("Hostname:", hostname)
        else:
            print("Error while getting hostname")
    except socket.herror:
        print("Error while getting hostname")
else:
    print("IP address is invalid")
