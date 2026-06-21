#!/usr/bin/env python

import socket
import sys
import re

if len(sys.argv) != 3:
    print("Usage: python3 7.py <server ip / hostname> <server port>")
    sys.exit(1)

server_host = sys.argv[1]
try:
    server_port = int(sys.argv[2])
except ValueError:
    print("Invalid port number")
    sys.exit(1)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        s.connect((server_host, server_port))

        try:
            service_name = socket.getservbyport(server_port, "tcp")
        except OSError:
            service_name = "unknown"

        print(f"Port {server_port} is open. Service name: {service_name}")

except socket.timeout:
    print(f"Port {server_port} is closed (Connection timed out)")
except ConnectionRefusedError:
    print(f"Port {server_port} is closed (Connection refused)")
except Exception:
    print(f"Port {server_port} is closed (Connection failed)")