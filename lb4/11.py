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
                    parts = msg.split(";")
                    response = "BAD_SYNTAX"
                    
                    if parts[0] == "zad15odpA":
                        # zad15odpA;ver;V;srcip;IP;dstip;IP;type;P
                        if len(parts) == 9 and parts[1] == "ver" and parts[3] == "srcip" and parts[5] == "dstip" and parts[7] == "type":
                            if parts[2] == "4" and parts[4] == "212.182.24.27" and parts[6] == "192.168.0.2" and parts[8] == "6":
                                response = "TAK"
                            else:
                                response = "NIE"
                                
                    elif parts[0] == "zad15odpB":
                        # zad15odpB;srcport;P1;dstport;P2;data;TRESC
                        if len(parts) == 7 and parts[1] == "srcport" and parts[3] == "dstport" and parts[5] == "data":
                            if parts[6] == "network programming is fun":
                                response = "TAK"
                            else:
                                response = "NIE"        
                except Exception:
                    response = "BAD_SYNTAX"
                
                s.sendto(response.encode("utf-8"), addr)
                print(f"Sent: {response} to {addr}")

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nUDP server stopped.")