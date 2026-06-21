#!/usr/bin/env python

import socket

server_host = "212.182.24.27"
server_port = 2908
MAX_PACKET_LENGTH = 20

def send_exactly(s, data):
    total_sent = 0
    while total_sent < len(data):
        sent = s.send(data[total_sent:])
        
        if sent == 0:
            raise RuntimeError("Connection lost while sending")
            
        total_sent += sent

def recv_exactly(sock, msg_len):
    msg = b""
    bytes_rcvd = 0
    
    while bytes_rcvd < msg_len:
        chunk = sock.recv(msg_len - bytes_rcvd)
        
        if not chunk:
            raise RuntimeError("Connection lost while receiving")
            
        bytes_rcvd += len(chunk)
        msg += chunk
        
    return msg

message = input("Message: ")
msg_bytes = message.encode('utf-8')
msg_bytes = msg_bytes[:MAX_PACKET_LENGTH].ljust(MAX_PACKET_LENGTH, b' ')

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        s.connect((server_host, server_port))

        send_exactly(s, msg_bytes)
        
        data = recv_exactly(s, MAX_PACKET_LENGTH)
        
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