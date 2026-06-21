#!/usr/bin/env python3

import socket

tcp_segment = "0b 54 89 8b 1f 9a 18 ec bb b1 64 f2 80 18 00 e3 67 71 00 00 01 01 08 0a 02 c1 a4 ee 00 1a 4c ee 68 65 6c 6c 6f 20 3a 29"

hex_data = tcp_segment.replace(" ", "")

src_port_hex = hex_data[0:4]
src_port = int(src_port_hex, 16)

dst_port_hex = hex_data[4:8]
dst_port = int(dst_port_hex, 16)

data_hex = hex_data[64:]
data = bytes.fromhex(data_hex).decode('utf-8')

message = f"zad13odp;src;{src_port};dst;{dst_port};data;{data}"

print(f"- Source port: {src_port}")
print(f"- Destination port: {dst_port}")
print(f"- Data: '{data}' ({len(data_hex)//2} bytes)\n")
print(f"Sent message: {message}")

server_host = "212.182.24.27"
server_port = 2909 

try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(5)
        
        s.sendto(message.encode('utf-8'), (server_host, server_port))
        
        response, addr = s.recvfrom(4096)
        
        if response:
            print("Server response:", response.decode('utf-8').strip())
        else:
            print("No response from the server")
except socket.timeout:
    print("Connection timed out")
except socket.gaierror:
    print("Error while resolving hostname")
except ConnectionRefusedError:
    print("Connection refused by the server")
except Exception as e:
    print(f"Connection failed: {e}")