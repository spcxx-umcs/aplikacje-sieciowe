#!/usr/bin/env python3

import socket
import time

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 2900

def recv_exact(conn, n):
    data = b''
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(1)
        
        print(f"Server is listening on {SERVER_HOST}:{SERVER_PORT}...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                
                data = recv_exact(conn, 20)
                if data:
                    conn.sendall(data)
                    print(f"Echo sent back to {addr}")

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nServer stopped.")