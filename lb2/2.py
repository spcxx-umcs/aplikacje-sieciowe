#!/usr/bin/env python

import socket

server_host = "212.182.24.27"
server_port = 2900
message = input("Message: ")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        s.connect((server_host, server_port))

        s.sendall(message.encode('utf-8'))
        
        data = s.recv(4096)
        
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