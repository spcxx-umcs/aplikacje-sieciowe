#!/usr/bin/env python3

import socket
import random

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 2912

def run_server():
    target_number = random.randint(1, 100)
    print(f"Server started. Target number is: {target_number}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(1)
        
        print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}...")
        
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            game_active = True
            
            while game_active:
                data = conn.recv(4096)
                if not data:
                    break
                
                message = data.decode('utf-8').strip()
                
                try:
                    guess = int(message)
                    
                    if guess < target_number:
                        response = "Too small"
                    elif guess > target_number:
                        response = "Too big"
                    else:
                        response = "Correct number"
                        game_active = False
                except ValueError:
                    response = "Error: Not a number"
                
                conn.sendall(response.encode('utf-8'))
                print(f"Sent: {response} to {addr}")
        
    print("Game is over, server stopping.")

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nServer stopped.")