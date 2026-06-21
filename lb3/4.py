#!/usr/bin/env python

import socket

server_host = "212.182.24.27"
server_port = 2901
message = input("Message: ")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(10)

        s.sendto(message.encode('utf-8'), (server_host, server_port))
        data, address = s.recvfrom(4096)
        
        if data:
            print(data.decode('utf-8').strip())
        else:
            print("No response from the server")
except socket.timeout:
    print("Connection timed out")
except socket.gaierror:
    print("Error while resolving hostname")
except ConnectionRefusedError:
    print("Connection refused by the server")
except Exception:
    print("Connection failed")