#!/usr/bin/env python3

import socket

SERVER_HOST = "httpbin.org"
PORT = 80
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"

def run_client():
    user_data = input("Provide data (key=value) (separated by &): ")
    
    body = user_data
    content_length = len(body)
    
    try:
        with socket.create_connection((SERVER_HOST, PORT)) as s:
            request = (
                "POST /post HTTP/1.1\r\n"
                f"Host: {SERVER_HOST}\r\n"
                f"User-Agent: {USER_AGENT}\r\n"
                "Content-Type: application/x-www-form-urlencoded\r\n"
                f"Content-Length: {content_length}\r\n"
                "Connection: close\r\n"
                "\r\n"
                f"{body}"
            )
            
            s.sendall(request.encode())
            
            response = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
            
            print("\nResponse from the server:")
            print(response.decode(errors="replace"))
                
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("\nStopping")