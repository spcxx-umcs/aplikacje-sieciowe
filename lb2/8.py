#!/usr/bin/env python

import socket
import sys
from concurrent.futures import ThreadPoolExecutor

def check_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((host, port))

            if result == 0:
                try:
                    service_name = socket.getservbyport(port, "tcp")
                except OSError:
                    service_name = "unknown"
                return (port, service_name)
    except Exception:
        pass

    return None

if len(sys.argv) != 2:
    print("Usage: python3 8.py <server ip / hostname>")
    sys.exit(1)

server_host = sys.argv[1]

print("Scanning ports...")

open_ports = []

with ThreadPoolExecutor(max_workers=100) as executor:
    results = executor.map(lambda p: check_port(server_host, p), range(1, 1025)) # lub 65536 - ale to zajmie dużo czasu

open_ports = [port for port in results if port is not None]

print("Open ports:")
for port, service in open_ports:
    print(f"- Port: {port:<5} Service name: {service}")