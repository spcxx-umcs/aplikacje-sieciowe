#!/usr/bin/env python

import socket
import time

server_host = "127.0.0.1"
tcp_port = 2900
udp_port = 2901

data_chunk = b"X" * 1024
iterations = 100000    

print("-- TCP --")
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        s.connect((server_host, tcp_port))
        print(f"Connected to {server_host}:{tcp_port}")
        
        start_time = time.time()
        for _ in range(iterations):
            s.sendall(data_chunk)
        end_time = time.time()
        
        print(f"TCP time: {end_time - start_time:.4f} s")
except socket.timeout:
    print("Connection timed out")
except socket.gaierror:
    print("Network address error")
except ConnectionRefusedError:
    print("Connection refused by the server")
except KeyboardInterrupt:
    print("\nStopping") 
except Exception:
    print("Connection failed")

print("\n-- UDP --")
try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        print(f"Sending UDP packets to {server_host}:{udp_port}")
        
        start_time = time.time()
        for _ in range(iterations):
            s.sendto(data_chunk, (server_host, udp_port))
        end_time = time.time()
        
        print(f"UDP time: {end_time - start_time:.4f} s")
except socket.timeout:
    print("Connection timed out")
except socket.gaierror:
    print("Network address error")
except ConnectionRefusedError:
    print("Connection refused by the server")
except KeyboardInterrupt:
    print("\nStopping") 
except Exception:
    print("Connection failed")