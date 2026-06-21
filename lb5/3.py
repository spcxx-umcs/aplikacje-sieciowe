#!/usr/bin/env python

import socket
import time
import itertools

server_host = "212.182.24.27"
tcp_port = 2913

found_ports = []
print("Scanning UDP ports...")

# wywnioskowalem z zadania, ze chodzi o to, ze skanujemy porty, ktore koncza sie cyframi 666, np. 666, 1666 itd.
for port in range(666, 65536, 1000):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_s:
            udp_s.settimeout(0.5)
            udp_s.sendto(b"PING", (server_host, port))
            data, _ = udp_s.recvfrom(1024)
            
            if data and data.decode('utf-8').strip() == "PONG":
                found_ports.append(port)
    except socket.timeout:
        continue
    except socket.gaierror:
        print("Network address error")
    except ConnectionRefusedError:
        print("Connection refused by the server")
    except KeyboardInterrupt:
        print("\nStopping") 
    except Exception:
        print("Connection failed")

print(f"Found responding ports: {found_ports}")

if found_ports:
    success = False
    for seq in itertools.permutations(found_ports):
        print(f"\nKnocking on ports (sequence: {seq})...")

        knock_failed = False
        for port in seq:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_s:
                    udp_s.sendto(b"PING", (server_host, port))
                time.sleep(0.1) 
            except Exception as e:
                print(f"UDP send error on port {port}: {e}")
                knock_failed = True
                break
            
        if knock_failed:
            continue

        print("Attempting TCP connection...")
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                s.connect((server_host, tcp_port))
                print(f"Connected to {server_host}:{tcp_port}")
                
                data = s.recv(4096)
                
                if data:
                    response = data.decode('utf-8').strip()
                    print("\nServer response:", response)
                    success = True
                    break
                else:
                    print("No response from the server")
        except socket.timeout:
            print("Connection timed out")
        except socket.gaierror:
            print("Network address error")
        except ConnectionRefusedError:
            print("Connection refused by the server")
        except KeyboardInterrupt:
            print("\nStopping") 
        except Exception:
            print("Connection failed")
    if not success:
        print("\nCould not access the hidden service.")
        
else:
    print("No ports found. Cannot knock.")