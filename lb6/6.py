#!/usr/bin/env python3

import socket
import ssl
import base64

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

    context = ssl.create_default_context() # ssl potrzebny, kazdy serwer potrzebuje teraz szyfrowania

    try:
        with socket.create_connection((SERVER_HOST, PORT)) as sock:
            welcome = sock.recv(4096).decode()
            if not welcome.startswith("220"):
                raise Exception(f"Server did not welcome us: {welcome}")

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
                    f"\r\n"
                    f"{body}\r\n"
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