#!/usr/bin/env python

import socket

server_host = "ntp.task.gda.pl"
server_port = 13

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        s.connect((server_host, server_port))

        data = s.recv(4096)
        
        if data:
            print(data.decode('utf-8').strip())
        else:
            print("No response from the server")
except socket.timeout:
    print("Connection timed out")
except socket.gaierror:
    print("Error while resolving hostname")
except Exception:
    print("Connection failed")