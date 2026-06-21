#!/usr/bin/env python3

import socket
import ssl
import re

SERVER_HOST = "imap.ethereal.email"
PORT = 993

EMAIL = "krystina1@ethereal.email"
PASSWORD = "hK5DCNzngvztC75eMf"

def send_cmd(s, tag, cmd):
    s.sendall(f"{tag} {cmd}\r\n".encode())
    
    response = ""
    while True:
        chunk = s.recv(4096).decode()
        response += chunk
        if f"{tag} OK" in response or f"{tag} BAD" in response or f"{tag} NO" in response:
            break
    return response

def run_client():
    context = ssl.create_default_context()
    tag = 1

    try:
        with socket.create_connection((SERVER_HOST, PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=SERVER_HOST) as s:
                welcome = s.recv(4096).decode()
                if not welcome.startswith("* OK"):
                    raise Exception(f"Server did not welcome us: {welcome.strip()}")

                send_cmd(s, f"A{tag}", f"LOGIN {EMAIL} {PASSWORD}")
                tag += 1

                list_response = send_cmd(s, f"A{tag}", 'LIST "" *')
                tag += 1
                
                mailboxes = re.findall(r'LIST .* "(.*)"', list_response)
                
                total_messages = 0
                
                print("-" * 10)
                for mb in mailboxes:
                    status_resp = send_cmd(s, f"A{tag}", f'STATUS "{mb}" (MESSAGES)')
                    tag += 1
                    
                    match = re.search(r'MESSAGES (\d+)', status_resp)
                    count = int(match.group(1)) if match else 0
                    
                    print(f"{mb:<20} | {count}")
                    total_messages += count
                
                print("-" * 10)
                print(f"Total messages: {total_messages}")

                send_cmd(s, f"A{tag}", "LOGOUT")
                print("Disconnected.")
                
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("\nStopping")