#!/usr/bin/env python3

import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 2901

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((SERVER_HOST, SERVER_PORT))
        
        print(f"UDP server is listening on {SERVER_HOST}:{SERVER_PORT}...")

        while True:
            data1_raw, addr = s.recvfrom(4096)
            op_raw, addr = s.recvfrom(4096)
            data2_raw, addr = s.recvfrom(4096)
            
            if data1_raw and op_raw and data2_raw:
                data1 = data1_raw.decode('utf-8').strip()
                op = op_raw.decode('utf-8').strip()
                data2 = data2_raw.decode('utf-8').strip()
                
                print(f"Received: {data1} {op} {data2} from {addr}")
                
                try:
                    num1 = float(data1)
                    num2 = float(data2)
                    
                    if op == '+': result = num1 + num2
                    elif op == '-': result = num1 - num2
                    elif op == '*': result = num1 * num2
                    elif op == '/': 
                        if num2 != 0:
                            result = num1 / num2
                        else:
                            result = "Error: Division by zero"
                    else: 
                        result = "Error: Unknown operator"
                    
                    response = str(result)
                except Exception:
                    response = "Error: Invalid format"
                
                s.sendto(response.encode('utf-8'), addr)
                print(f"Result sent: {response} to {addr}")

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nUDP server stopped.")