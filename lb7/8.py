#!/usr/bin/env python3

import socket
import ssl

SERVER_HOST = "pop3.ethereal.email"
PORT = 995

EMAIL = "krystina1@ethereal.email"
PASSWORD = "hK5DCNzngvztC75eMf"

def send_cmd(s, cmd, expected_prefix="+OK", multiline=False):
    s.sendall((cmd + "\r\n").encode())
    
    response_data = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        response_data += chunk
        
        if not multiline and b"\r\n" in response_data:
            break
        if multiline and b"\r\n.\r\n" in response_data:
            break
            
    response = response_data.decode()
    
    if expected_prefix:
        if not response.startswith(expected_prefix):
            raise Exception(f"Server rejected command '{cmd}': {response.strip()}")
            
    return response

def run_client():
    context = ssl.create_default_context()

    try:
        with socket.create_connection((SERVER_HOST, PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=SERVER_HOST) as s:
                welcome = s.recv(4096).decode()
                if not welcome.startswith("+OK"):
                    raise Exception(f"Server did not welcome us: {welcome.strip()}")

                send_cmd(s, f"USER {EMAIL}")
                send_cmd(s, f"PASS {PASSWORD}")
                
                list_response = send_cmd(s, "LIST", multiline=True)
                
                lines = list_response.splitlines()
                
                for line in lines[1:-1]:
                    if line.strip() == ".": 
                        continue
                        
                    parts = line.split()
                    if len(parts) >= 2:
                        msg_id = parts[0]
                        msg_size = parts[1]
                        print(f"Message nr {msg_id}: {msg_size} bytes")
                
                send_cmd(s, "QUIT")
                print("Disconnected.")
                
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("\nStopping")