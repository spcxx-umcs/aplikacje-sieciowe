#!/usr/bin/env python3

import socket
import base64

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 2902

TEST_USER = "enya.vonrueden@ethereal.email"
TEST_PASS = "YKujV2SpeeN69D5ckM"

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(5)
        
        print(f"SMTP server listening on {SERVER_HOST}:{SERVER_PORT}...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                conn.sendall(b"220 SMTP Ready\r\n")
                
                state = {"auth_step": 0, "data_mode": False, "mail_buffer": []}
                
                while True:
                    data = conn.recv(4096)
                    if not data: break
                    
                    lines = data.decode("utf-8", errors="replace").splitlines()
                    
                    for cmd in lines:
                        cmd = cmd.strip()
                        if not cmd and not state["data_mode"]: continue
                        print(f"Received: {cmd}")
                        
                        if state["data_mode"]:
                            if cmd == ".":
                                conn.sendall(b"250 Message accepted\r\n")
                                print("--- EMAIL RECEIVED ---")
                                print("\n".join(state["mail_buffer"]))
                                print("----------------------")
                                state["data_mode"] = False
                                state["mail_buffer"] = []
                            else:
                                state["mail_buffer"].append(cmd)
                        
                        elif state["auth_step"] == 1:
                            state["auth_step"] = 2
                            conn.sendall(b"334 UGFzc3dvcmQ6\r\n")
                        elif state["auth_step"] == 2:
                            conn.sendall(b"235 Authentication successful\r\n")
                            state["auth_step"] = 0
                        elif cmd.upper().startswith("EHLO"):
                            conn.sendall(b"250 OK\r\n")
                        elif cmd.upper().startswith("STARTTLS"):
                            conn.sendall(b"220 Ready to start TLS\r\n")
                        elif cmd.upper().startswith("AUTH LOGIN"):
                            conn.sendall(b"334 VXNlcm5hbWU6\r\n")
                            state["auth_step"] = 1
                        elif cmd.upper().startswith("MAIL FROM"):
                            conn.sendall(b"250 Accepted\r\n")
                        elif cmd.upper().startswith("RCPT TO"):
                            conn.sendall(b"250 Accepted\r\n")
                        elif cmd.upper().startswith("DATA"):
                            state["data_mode"] = True
                            conn.sendall(b"354 End data with .\r\n")
                        elif cmd.upper().startswith("QUIT"):
                            conn.sendall(b"221 Bye\r\n")
                            break
                        else:
                            conn.sendall(b"502 Command not implemented\r\n")
        print("Connection closed.\n")

if __name__ == "__main__":
    try: 
        run_server()
    except KeyboardInterrupt: 
        print("\nStopped.")