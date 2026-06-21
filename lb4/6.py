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
                hostname = data.decode('utf-8').strip()
                print(f"Received hostname: {hostname} from {addr}")
                
                try:
                    ip_address = socket.gethostbyname(hostname)
                    response = ip_address
                except socket.gaierror:
                    response = "Error: Hostname not found"
                except Exception as e:
                    response = f"Error: {str(e)}"
                
                s.sendto(response.encode('utf-8'), addr)
                print(f"Sent IP: {response} to {addr}")

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nUDP server stopped.")