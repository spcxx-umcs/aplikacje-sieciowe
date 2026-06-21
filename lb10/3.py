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

def send_frame(s, message):
    message_bytes = message.encode('utf-8')
    length = len(message_bytes)
    
    frame = bytearray([0x81])

    if length <= 125:
        frame.append(0x80 | length)
    elif length <= 65535:
        frame.append(0x80 | 126)
        # 2B
        frame.append((length >> 8) & 0xFF)
        frame.append(length & 0xFF)
    else:
        frame.append(0x80 | 127)
        # 8B
        for i in range(7, -1, -1):
            frame.append((length >> (i * 8)) & 0xFF)
    
    masking_key = os.urandom(4)
    frame.extend(masking_key)
    
    for i in range(length):
        frame.append(message_bytes[i] ^ masking_key[i % 4])
    
    s.sendall(frame)

def run_client():
    ws_key = base64.b64encode(os.urandom(16)).decode('utf-8')
    
    message = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris "
        "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in "
        "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
    )
    
    try:
        with socket.create_connection((SERVER_HOST, SERVER_PORT)) as s:
            print(f"Connecting to {SERVER_HOST}:{SERVER_PORT}...")
            
            perform_handshake(s, SERVER_HOST, ws_key)
            
            print("Handshake successful.")
            
            send_frame(s, message)
            print(f"Message sent (length {len(message)}): {message}")
            
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("\nStopping")