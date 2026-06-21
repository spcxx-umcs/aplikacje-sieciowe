#!/usr/bin/env python3

import socket
import os

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
FILES_DIR = "7_files"

def load_file(filename):
    try:
        path = os.path.join(FILES_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"<html><body><h1>{filename} not found</h1></body></html>"

def send_response(conn, status_code, reason, body):
    header = f"HTTP/1.1 {status_code} {reason}\r\n"
    header += "Content-Type: text/html\r\n"
    header += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
    header += "Connection: close\r\n"
    header += "\r\n"
    conn.sendall((header + body).encode("utf-8"))

def send_head_response(conn, status_code, reason, content_length):
    header = f"HTTP/1.1 {status_code} {reason}\r\n"
    header += "Content-Type: text/html\r\n"
    header += f"Content-Length: {content_length}\r\n"
    header += "Connection: close\r\n"
    header += "\r\n"
    conn.sendall(header.encode("utf-8"))

def run_server():
    if not os.path.exists(FILES_DIR):
        print(f"{FILES_DIR} does not exist")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(1)
        print(f"HTTP server listening on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(4096)
                if not data: continue
                
                request_lines = data.decode("utf-8", errors="replace").splitlines()
                if not request_lines: continue
                
                parts = request_lines[0].split()
                if len(parts) < 3:
                    send_response(conn, 400, "Bad Request", load_file("400.html"))
                    continue
                
                method, path, version = parts
                print(f"[{addr}] {method} {path}")

                headers = {}
                for line in request_lines[1:]:
                    if not line: break
                    if ": " in line:
                        key, val = line.split(": ", 1)
                        headers[key.lower()] = val
                
                for h, v in headers.items():
                    print(f"   Header -> {h}: {v}")

                if method == "GET":
                    if path == "/":
                        send_response(conn, 200, "OK", load_file("index.html"))
                    elif path == "/page":
                        send_response(conn, 200, "OK", load_file("page.html"))
                    else:
                        send_response(conn, 404, "Not Found", load_file("404.html"))

                elif method == "HEAD":
                    body = load_file("index.html" if path == "/" else "page.html" if path == "/page" else "404.html")
                    send_head_response(conn, 200, "OK", len(body.encode('utf-8')))

                elif method == "POST":
                    if b"\r\n\r\n" in data:
                        _, body_bytes = data.split(b"\r\n\r\n", 1)
                        print(f"   POST Body received ({len(body_bytes)} bytes): {body_bytes.decode('utf-8', errors='ignore')[:50]}...")
                        send_response(conn, 200, "OK", "<h1>POST received</h1>")
                    else:
                        send_response(conn, 400, "Bad Request", "<h1>Missing POST body</h1>")

                elif method == "OPTIONS":
                    header = "HTTP/1.1 200 OK\r\n"
                    header += "Allow: GET, HEAD, POST, OPTIONS\r\n"
                    header += "Content-Length: 0\r\n"
                    header += "Connection: close\r\n\r\n"
                    conn.sendall(header.encode("utf-8"))

                else:
                    send_response(conn, 405, "Method Not Allowed", "<h1>405 Method Not Allowed</h1>")

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nStopped.")