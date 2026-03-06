#!/usr/bin/env python

import re

user_ip = str(input("IP address: "))
valid = re.search( r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", user_ip)

if valid:
    print("IP address is valid")
else:
    print("IP address is invalid")