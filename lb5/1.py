#!/usr/bin/env python

import socket

server_host = "212.182.24.27"
server_port = 2912

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        s.connect((server_host, server_port))
        print(f"Connected to {server_host}:{server_port}")

        while True:
            guess = input("Enter the number to guess: ")
            
            s.sendall(guess.encode('utf-8'))
            data = s.recv(4096)
            
            if data:
                response = data.decode('utf-8').strip()
                print(response)
                
                if response == "Correct number":
                    break
            else:
                print("No response from the server")
                break
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