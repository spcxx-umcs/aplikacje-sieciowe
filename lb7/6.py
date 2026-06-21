#!/usr/bin/env python3

import socket
import ssl

SERVER_HOST = "pop3.ethereal.email"
PORT = 995

EMAIL = "krystina1@ethereal.email"
PASSWORD = "hK5DCNzngvztC75eMf"

def send_cmd(s, cmd, expected_prefix="+OK"):
    s.sendall((cmd + "\r\n").encode())
    response = s.recv(4096).decode()
    
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
                
                stat_response = send_cmd(s, "STAT")
                
                parts = stat_response.split()
                
                if len(parts) >= 2:
                    msg_count = parts[1]
                    print(f"Messages in mailbox: {msg_count}")
                else:
                    print("Error while analyzing STAT.")
                
                send_cmd(s, "QUIT")
                print("Disconnected.")
                
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("\nStopping")