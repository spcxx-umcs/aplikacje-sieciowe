#!/usr/bin/env python3

import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8143

messages = [
    {"id": 1, "content": "From: a@test.edu\r\nSubject: Test1\r\n\r\nWitaj 1\r\n", "flags": set()},
    {"id": 2, "content": "From: b@test.edu\r\nSubject: Test2\r\n\r\nWitaj 2\r\n", "flags": set()}
]

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(1)
        print(f"IMAP Server active on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                conn.sendall(b"* OK IMAP4rev1 Service Ready\r\n")
                authenticated = False
                selected = False
                
                while True:
                    data = conn.recv(4096)
                    if not data: break
                    
                    for cmd_line in data.decode("utf-8", errors="replace").splitlines():
                        cmd_line = cmd_line.strip()
                        if not cmd_line: continue
                        
                        parts = cmd_line.split(maxsplit=2)
                        tag = parts[0]
                        cmd = parts[1].upper()
                        arg = parts[2] if len(parts) > 2 else ""
                        
                        print(f"[{tag}] {cmd} {arg}")

                        if cmd == "LOGIN":
                            authenticated = True
                            conn.sendall(f"{tag} OK LOGIN completed\r\n".encode())
                        
                        elif cmd == "SELECT":
                            selected = True
                            conn.sendall(f"* {len(messages)} EXISTS\r\n".encode())
                            conn.sendall(f"{tag} OK [READ-WRITE] SELECT completed\r\n".encode())

                        elif cmd == "LIST":
                            conn.sendall(b'* LIST () "/" "INBOX"\r\n')
                            conn.sendall(f"{tag} OK LIST completed\r\n".encode())
                        elif cmd == "FETCH":
                            try:
                                msg_id = int(arg.split()[0])
                                msg = next((m for m in messages if m["id"] == msg_id), None)
                                if msg:
                                    content = msg["content"]
                                    conn.sendall(f"* {msg_id} FETCH (BODY[TEXT] {{{len(content)}}}\r\n{content})\r\n".encode())
                                    conn.sendall(f"{tag} OK FETCH completed\r\n".encode())
                                else:
                                    conn.sendall(f"{tag} NO Message not found\r\n".encode())
                            except:
                                conn.sendall(f"{tag} BAD Invalid FETCH parameters\r\n".encode())

                        elif cmd == "SEARCH":
                            unseen = [str(m["id"]) for m in messages if "\\Seen" not in m["flags"]]
                            conn.sendall(f"* SEARCH {' '.join(unseen)}\r\n".encode())
                            conn.sendall(f"{tag} OK SEARCH completed\r\n".encode())

                        elif cmd == "STORE":
                            try:
                                parts = arg.split()
                                msg_id = int(parts[0])
                                flag = parts[2].strip("()")
                                msg = next((m for m in messages if m["id"] == msg_id), None)
                                if msg:
                                    if "+" in arg: msg["flags"].add(flag)
                                    else: msg["flags"].discard(flag)
                                conn.sendall(f"* {msg_id} FETCH (FLAGS ({' '.join(msg['flags'])}))\r\n".encode())
                                conn.sendall(f"{tag} OK STORE completed\r\n".encode())
                            except:
                                conn.sendall(f"{tag} BAD Invalid STORE parameters\r\n".encode())

                        elif cmd == "EXPUNGE":
                            to_remove = [m for m in messages if "\\Deleted" in m["flags"]]
                            for m in to_remove:
                                conn.sendall(f"* {m['id']} EXPUNGE\r\n".encode())
                                messages.remove(m)
                            conn.sendall(f"{tag} OK EXPUNGE completed\r\n".encode())

                        elif cmd == "STATUS":
                            conn.sendall(f"* STATUS INBOX (MESSAGES {len(messages)})\r\n".encode())
                            conn.sendall(f"{tag} OK STATUS completed\r\n".encode())
                            
                        elif cmd == "LOGOUT":
                            conn.sendall(b"* BYE Logout requested\r\n")
                            conn.sendall(f"{tag} OK LOGOUT completed\r\n".encode())
                            break
                        
                        else:
                            conn.sendall(f"{tag} BAD Unknown command\r\n".encode())

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nStopped.")