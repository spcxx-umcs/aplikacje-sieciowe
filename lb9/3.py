#!/usr/bin/env python3

import socket
import re

SERVER_HOST = "212.182.24.27"
PORT = 8080
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"

def get_file_size():
    try:
        with socket.create_connection((SERVER_HOST, PORT)) as s:
            request = (
                "HEAD /image.jpg HTTP/1.1\r\n"
                f"Host: {SERVER_HOST}:{PORT}\r\n"
                f"User-Agent: {USER_AGENT}\r\n"
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
            
            match = re.search(rb"Content-Length: (\d+)", response, re.IGNORECASE)
            return int(match.group(1)) if match else 0
    except Exception as e:
        print(f"HEAD request failed: {e}")
        return 0

def fetch_part(start, end):
    with socket.create_connection((SERVER_HOST, PORT)) as s:
        request = (
            "GET /image.jpg HTTP/1.1\r\n"
            f"Host: {SERVER_HOST}:{PORT}\r\n"
            f"User-Agent: {USER_AGENT}\r\n"
            f"Range: bytes={start}-{end}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        s.sendall(request.encode())
        
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk: break
            response += chunk
            
        _, body = response.split(b"\r\n\r\n", 1)
        return body

def run_client():
    total_size = get_file_size()

    chunk_size = total_size // 3
    parts = [
        (0, chunk_size),
        (chunk_size + 1, 2 * chunk_size),
        (2 * chunk_size + 1, total_size - 1)
    ]

    full_image = b""
    for i, (start, end) in enumerate(parts):
        print(f"Downloading part {i+1}...")
        full_image += fetch_part(start, end)

    with open("image_2.jpg", "wb") as f:
        f.write(full_image)
    print("Image saved to image_2.jpg")

if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("\nStopping")