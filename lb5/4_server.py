#!/usr/bin/env python3

import socket

SERVER_HOST = "127.0.0.1"
TCP_PORT = 2900
UDP_PORT = 2901

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_s:
        tcp_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_s.bind((SERVER_HOST, TCP_PORT))
        tcp_s.listen(1)
        
        print(f"TCP server is listening on {SERVER_HOST}:{TCP_PORT}...")
        conn, addr = tcp_s.accept()
        
        with conn:
            print(f"TCP Connected by {addr}")
            while True:
                data = conn.recv(4096)
                if not data:
                    break
        print("TCP data received and connection closed.\n")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_s:
        udp_s.bind((SERVER_HOST, UDP_PORT))
        udp_s.settimeout(3) 
        
        print(f"UDP server is listening on {SERVER_HOST}:{UDP_PORT}...")
        while True:
            try:
                data, addr = udp_s.recvfrom(4096)
            except socket.timeout:
                print("UDP data stream finished (timeout).")
                break
            except Exception:
                break

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nServer stopped.")