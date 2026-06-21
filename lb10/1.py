#!/usr/bin/env python3

import socket
import base64
import os

SERVER_HOST = "echo.websocket.org"
SERVER_PORT = 80

def perform_handshake(s, host, key):
    handshake_request = (
        "GET / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "\r\n"
    )
    
    s.sendall(handshake_request.encode())
    response = s.recv(4096).decode()
    
    if "101 Switching Protocols" not in response:
        raise Exception(f"Handshake failed. Server response:\n{response}")
            
    return response

def run_client():
    ws_key = base64.b64encode(os.urandom(16)).decode('utf-8')
    
    try:
        with socket.create_connection((SERVER_HOST, SERVER_PORT)) as s:
            print(f"Connecting to {SERVER_HOST}:{SERVER_PORT}...")
            
            response = perform_handshake(s, SERVER_HOST, ws_key)
            
            print("Handshake successful.")
            print("Server response:\n")
            print(response.strip())
            print("")
            
            print("Connection established.")
            
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("\nStopping")