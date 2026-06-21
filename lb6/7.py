#!/usr/bin/env python3

import socket
import ssl
import base64
import os

SERVER_HOST = "smtp.ethereal.email"
PORT = 587

EMAIL = "kenya.vonrueden@ethereal.email"
PASSWORD = "YKujV2SpeeN69D5ckM"

def send_cmd(s, cmd, expected_codes=None):
    s.sendall((cmd + "\r\n").encode())
    response = s.recv(4096).decode()
    
    if expected_codes:
        code = response[:3]
        if code not in expected_codes:
            raise Exception(f"Server rejected command '{cmd}': {response.strip()}")
    return response

def run_client():
    sender = input("Sender address: ")
    recipient_input = input("Recipient addresses (comma separated): ")
    recipients = [r.strip() for r in recipient_input.split(',')]
    subject = input("Subject: ")
    body = input("Message content: ")

    file_path = input("Path to text file: ")
    if not os.path.exists(file_path):
        print("File not found")
        return

    with open(file_path, "r") as f:
        file_content = f.read()
    file_encoded = base64.b64encode(file_content.encode()).decode()

    boundary = "MIME_BOUNDARY_MIME"
    context = ssl.create_default_context()

    try:
        with socket.create_connection((SERVER_HOST, PORT)) as sock:
            if not sock.recv(4096).decode().startswith("220"):
                raise Exception("Server refused connection")

            send_cmd(sock, "EHLO szymonrozga", ["250"])
            send_cmd(sock, "STARTTLS", ["220"])
            
            with context.wrap_socket(sock, server_hostname=SERVER_HOST) as s:
                send_cmd(s, "EHLO szymonrozga", ["250"])
                send_cmd(s, "AUTH LOGIN", ["334"])
                send_cmd(s, base64.b64encode(EMAIL.encode()).decode(), ["334"])
                send_cmd(s, base64.b64encode(PASSWORD.encode()).decode(), ["235"])
                
                send_cmd(s, f"MAIL FROM: <{sender}>", ["250"])
                for r in recipients:
                    send_cmd(s, f"RCPT TO: <{r}>", ["250"])
                
                send_cmd(s, "DATA", ["354"])
                
                recipients_str = ", ".join(recipients)
                mail_content = (
                    f"From: {sender}\r\n"
                    f"To: {recipients_str}\r\n"
                    f"Subject: {subject}\r\n"
                    f"MIME-Version: 1.0\r\n"
                    f"Content-Type: multipart/mixed; boundary=\"{boundary}\"\r\n"
                    f"\r\n"
                    f"--{boundary}\r\n"
                    f"Content-Type: text/plain; charset=\"utf-8\"\r\n"
                    f"\r\n"
                    f"{body}\r\n"
                    f"\r\n"
                    f"--{boundary}\r\n"
                    f"Content-Type: text/plain; name=\"{os.path.basename(file_path)}\"\r\n"
                    f"Content-Disposition: attachment; filename=\"{os.path.basename(file_path)}\"\r\n"
                    f"Content-Transfer-Encoding: base64\r\n"
                    f"\r\n"
                    f"{file_encoded}\r\n"
                    f"\r\n"
                    f"--{boundary}--\r\n"
                    f".\r\n"
                )

                s.sendall(mail_content.encode())
                response = s.recv(4096).decode()
                if not response.startswith("250"):
                    raise Exception(f"Server rejected message: {response.strip()}")
                
                send_cmd(s, "QUIT", ["221"])
                print("Message sent.")
                
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("\nStopping")