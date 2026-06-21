#!/usr/bin/env python3

import socket

server_host = "212.182.24.27"
server_port = 2906

ip_to_check = input("IP address: ")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(10)

        s.sendto(ip_to_check.encode('utf-8'), (server_host, server_port))
        
        data, address = s.recvfrom(4096)
        
        if data:
            print("Server response (hostname):", data.decode('utf-8').strip())
        else:
            print("No response from the server")

except socket.timeout:
    print("Connection timed out")
except socket.gaierror:
    print("Error while resolving server hostname")
except ConnectionRefusedError:
    print("Connection refused by the server")
except KeyboardInterrupt:
    print("\nStopping") 
except Exception as e:
    print(f"Connection failed: {e}")