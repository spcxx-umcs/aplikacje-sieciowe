#!/usr/bin/env python3

import socket
import ssl

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

                # 2. Login
                send_cmd(s, f"A{tag}", f"LOGIN {EMAIL} {PASSWORD}")
                tag += 1

                response = send_cmd(s, f"A{tag}", "SELECT INBOX")
                tag += 1
                
                msg_count = 0
                for line in response.splitlines():
                    if "EXISTS" in line:
                        parts = line.split()
                        msg_count = parts[1]
                        break
                
                print(f"Messages in INBOX: {msg_count}")

                send_cmd(s, f"A{tag}", "LOGOUT")
                print("Disconnected.")
                
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("\nStopping")