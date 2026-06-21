#!/usr/bin/env python3

import socket
import time

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 2900

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
                
                data = conn.recv(4096)
                if data:
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    conn.sendall(current_time.encode('utf-8'))
                    print(f"Sent time: {current_time} to {addr}")

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nServer stopped.")