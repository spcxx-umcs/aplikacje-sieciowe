#!/usr/bin/env python3

import socket
import hashlib
import base64

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9000
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

def perform_handshake(conn, data):
    headers = {}
    lines = data.decode().splitlines()
    for line in lines[1:]:
        if ": " in line:
            key, val = line.split(": ", 1)
            headers[key.lower()] = val
            
    ws_key = headers.get("sec-websocket-key")
    if not ws_key:
        return False
        
    accept_key = base64.b64encode(hashlib.sha1((ws_key + GUID).encode()).digest()).decode()
    
    response = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Accept: {accept_key}\r\n"
        "\r\n"
    )
    conn.sendall(response.encode())
    return True

def decode_frame(data):
    payload_len = data[1] & 0x7F
    offset = 2

    if payload_len == 126:
        payload_len = (data[2] << 8) | data[3]
        offset = 4
    elif payload_len == 127:
        payload_len = int.from_bytes(data[2:10], byteorder='big')
        offset = 10
    
    mask_key = data[offset : offset + 4]
    payload = data[offset + 4 : offset + 4 + payload_len]
    
    decoded = bytearray()
    for i in range(len(payload)):
        decoded.append(payload[i] ^ mask_key[i % 4])
        
    return decoded.decode("utf-8")

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(1)
        print(f"WebSocket server listening on {SERVER_HOST}:{SERVER_PORT}...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                
                data = conn.recv(4096)
                if not data: break
                
                if perform_handshake(conn, data):
                    print("Handshake successful. Waiting for frames...")
                    
                    while True:
                        frame = conn.recv(4096)
                        if not frame:
                            break
                        
                        message = decode_frame(frame)
                        print(f"Received message: {message}")
                else:
                    print("Handshake failed.")
                    break
        print("Connection closed.")

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nStopped.")