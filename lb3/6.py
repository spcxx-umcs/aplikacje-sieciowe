#!/usr/bin/env python

import socket

server_host = "12.182.24.27"
server_port = 2902

number1 = input("First number: ")
operator = input("Operator (+, -, *, /): ")
number2 = input("Second number: ")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(10)

        s.sendto(number1.encode('utf-8'), (server_host, server_port))
        s.sendto(operator.encode('utf-8'), (server_host, server_port))
        s.sendto(number2.encode('utf-8'), (server_host, server_port))
        
        data, address = s.recvfrom(4096)
        
        if data:
            print("Result:", data.decode('utf-8').strip())
        else:
            print("No response from the server")

except socket.timeout:
    print("Connection timed out")
except socket.gaierror:
    print("Error while resolving hostname")
except ConnectionRefusedError:
    print("Connection refused by the server")
except KeyboardInterrupt:
    print("\nStopping") 
except Exception:
    print("Connection failed")