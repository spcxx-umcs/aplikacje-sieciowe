#!/usr/bin/env python3

import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8110

MESSAGES = [
    "From: a@test.edu\r\nSubject: Test1\r\n\r\nWitaj\r\n",
    "From: b@test.edu\r\nSubject: Test2\r\n\r\nWitaj 2\r\n",
    (
        "From: c@test.edu\r\n"
        "Subject: Test3\r\n"
        "MIME-Version: 1.0\r\n"
        "Content-Type: multipart/mixed; boundary=\"MIME-BOUNDARY-MIME\"\r\n"
        "\r\n"
        "--MIME-BOUNDARY-MIME\r\n"
        "Content-Type: text/plain; charset=utf-8\r\n"
        "\r\n"
        "Witaj 3\r\n"
        "\r\n"
        "--MIME-BOUNDARY-MIME\r\n"
        "Content-Type: image/png; name=\"obrazek.png\"\r\n"
        "Content-Disposition: attachment; filename=\"obrazek.png\"\r\n"
        "Content-Transfer-Encoding: base64\r\n"
        "\r\n"
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=\r\n"
        "--MIME-BOUNDARY-MIME--\r\n"
    )
]

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(1)
        
        print(f"POP3 server listening on {SERVER_HOST}:{SERVER_PORT}...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                
                conn.sendall(b"+OK POP3 server ready\r\n")
                
                state = {"authenticated": False}
                
                while True:
                    data = conn.recv(4096)
                    if not data: break
                    
                    lines = data.decode("utf-8", errors="replace").splitlines()
                    
                    for cmd_line in lines:
                        cmd_line = cmd_line.strip()
                        if not cmd_line: continue
                        print(f"Received: {cmd_line}")
                        
                        parts = cmd_line.split(maxsplit=1)
                        cmd = parts[0].upper()
                        arg = parts[1] if len(parts) > 1 else None
                        
                        if cmd == "USER":
                            conn.sendall(b"+OK User accepted\r\n")
                        
                        elif cmd == "PASS":
                            state["authenticated"] = True
                            conn.sendall(b"+OK Password accepted\r\n")
                        
                        elif cmd == "STAT":
                            if not state["authenticated"]:
                                conn.sendall(b"-ERR Not authenticated\r\n")
                            else:
                                total_size = sum(len(m) for m in MESSAGES)
                                conn.sendall(f"+OK {len(MESSAGES)} {total_size}\r\n".encode())
                        
                        elif cmd == "LIST":
                            if not state["authenticated"]:
                                conn.sendall(b"-ERR Not authenticated\r\n")
                            else:
                                total_size = sum(len(m) for m in MESSAGES)
                                conn.sendall(f"+OK {len(MESSAGES)} messages ({total_size} octets)\r\n".encode())
                                for i, msg in enumerate(MESSAGES):
                                    conn.sendall(f"{i+1} {len(msg)}\r\n".encode())
                                conn.sendall(b".\r\n")
                        
                        elif cmd == "RETR":
                            if not state["authenticated"]:
                                conn.sendall(b"-ERR Not authenticated\r\n")
                            elif arg:
                                try:
                                    idx = int(arg) - 1
                                    if 0 <= idx < len(MESSAGES):
                                        msg = MESSAGES[idx]
                                        conn.sendall(f"+OK {len(msg)} octets\r\n".encode())
                                        conn.sendall(msg.encode())
                                        conn.sendall(b".\r\n")
                                    else:
                                        conn.sendall(b"-ERR No such message\r\n")
                                except ValueError:
                                    conn.sendall(b"-ERR Invalid argument\r\n")
                            else:
                                conn.sendall(b"-ERR Missing argument\r\n")
                        
                        elif cmd == "DELE":
                            if not state["authenticated"]:
                                conn.sendall(b"-ERR Not authenticated\r\n")
                            elif arg:
                                try:
                                    idx = int(arg) - 1
                                    if 0 <= idx < len(MESSAGES):
                                        conn.sendall(f"+OK message {idx+1} deleted\r\n".encode())
                                    else:
                                        conn.sendall(b"-ERR No such message\r\n")
                                except ValueError:
                                    conn.sendall(b"-ERR Invalid argument\r\n")
                            else:
                                conn.sendall(b"-ERR Missing argument\r\n")
                        elif cmd == "QUIT":
                            conn.sendall(b"+OK POP3 server signing off\r\n")
                            break
                        
                        else:
                            conn.sendall(b"-ERR Command not implemented\r\n")
                            
        print("Connection closed.\n")

if __name__ == "__main__":
    try: 
        run_server()
    except KeyboardInterrupt: 
        print("\nStopped.")