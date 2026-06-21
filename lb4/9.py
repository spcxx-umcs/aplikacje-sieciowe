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
                msg = data.decode("utf-8").strip()
                print(f"Received: '{msg}' from {addr}")
                
                try:
                    # zad14odp;src;P1;dst;P2;data;TRESC
                    parts = msg.split(";")
                    
                    if len(parts) == 7 and parts[0] == "zad14odp" and parts[1] == "src" and parts[3] == "dst" and parts[5] == "data":
                        src_port = int(parts[2])
                        dst_port = int(parts[4])
                        content = parts[6]
                        
                        if content == "programming in python is fun":
                            response = "TAK"
                        else:
                            response = "NIE"
                    else:
                        response = "BAD_SYNTAX"
                except Exception:
                    response = "BAD_SYNTAX"
                
                s.sendto(response.encode("utf-8"), addr)
                print(f"Sent: {response} to {addr}")

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nUDP server stopped.")