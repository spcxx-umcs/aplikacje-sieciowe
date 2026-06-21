#!/usr/bin/env python3

import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 2901

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((SERVER_HOST, SERVER_PORT))
        
        print(f"UDP server is listening on {SERVER_HOST}:{SERVER_PORT}...")

        while True:
            data, addr = s.recvfrom(4096)
            
            if data:
                print(f"Received {len(data)} bytes from {addr}: {data.decode('utf-8').strip()}")
                s.sendto(data, addr)
                print(f"Echo sent back to {addr}")

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nUDP server stopped.")