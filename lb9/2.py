#!/usr/bin/env python3

import socket
import re

SERVER_HOST = "httpbin.org"
PORT = 80
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"

def run_client():
    try:
        with socket.create_connection((SERVER_HOST, PORT)) as s:
            request = (
                "GET /image/png HTTP/1.1\r\n"
                f"Host: {SERVER_HOST}\r\n"
                f"User-Agent: {USER_AGENT}\r\n"
                "Accept: image/png\r\n"
                "Connection: close\r\n"
                "\r\n"
            )
            
            s.sendall(request.encode())
            
            response = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
            
            if b"\r\n\r\n" in response:
                headers, body = response.split(b"\r\n\r\n", 1)
                
                with open("image.png", "wb") as f:
                    f.write(body)
                
                print("Image saved to image.png")
            else:
                print("Invalid HTTP response.")
                
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("\nStopping")