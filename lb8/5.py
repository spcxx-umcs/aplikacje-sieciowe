#!/usr/bin/env python3

import socket
import ssl
import re

SERVER_HOST = "127.0.0.1"
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

                send_cmd(s, f"A{tag}", "SELECT INBOX")
                tag += 1

                msg_id = input("Message number to delete: ")

                send_cmd(s, f"A{tag}", f"STORE {msg_id} +FLAGS (\\Deleted)")
                tag += 1
                
                send_cmd(s, f"A{tag}", "EXPUNGE")
                tag += 1
                
                print(f"Message deleted.")

                send_cmd(s, f"A{tag}", "LOGOUT")
                print("Disconnected.")
                
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("\nStopping")