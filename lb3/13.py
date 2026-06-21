#!/usr/bin/env python3

import socket

udp_datagram = "ed 74 0b 55 00 24 ef fd 70 72 6f 67 72 61 6d 6d 69 6e 67 20 69 6e 20 70 79 74 68 6f 6e 20 69 73 20 66 75 6e"

hex_data = udp_datagram.replace(" ", "")

src_port_hex = hex_data[0:4]
src_port = int(src_port_hex, 16)

dst_port_hex = hex_data[4:8]
dst_port = int(dst_port_hex, 16)

data_hex = hex_data[16:]
data = bytes.fromhex(data_hex).decode('utf-8')

message = f"zad14odp;src;{src_port};dst;{dst_port};data;{data}"

print(f"- Source port: {src_port}")
print(f"- Destination port: {dst_port}")
print(f"- Data: '{data}' ({len(data_hex)//2} bytes)\n")
print(f"Sent message: {message}")

server_host = "212.182.24.27"
server_port = 2910

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
except Exception:
    print("Connection failed")