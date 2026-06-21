#!/usr/bin/env python3

import socket

packet = "45 00 00 4e f7 fa 40 00 38 06 9d 33 d4 b6 18 1b c0 a8 00 02 0b 54 b9 a6 fb f9 3c 57 c1 0a 06 c1 80 18 00 e3 ce 9c 00 00 01 01 08 0a 03 a6 eb 01 00 0b f8 e5 6e 65 74 77 6f 72 6b 20 70 72 6f 67 72 61 6d 6d 69 6e 67 20 69 73 20 66 75 6e"
data = packet.replace(" ", "")

version = int(data[0], 16)
src_ip = ".".join([str(int(data[i:i+2], 16)) for i in range(24, 32, 2)])
dst_ip = ".".join([str(int(data[i:i+2], 16)) for i in range(32, 40, 2)])
protocol = int(data[18:20], 16)

tcp_start = 40
src_port = int(data[tcp_start:tcp_start+4], 16)
dst_port = int(data[tcp_start+4:tcp_start+8], 16)

if protocol == 6: # tcp
    data_start = tcp_start + 64
elif protocol == 17: # udp
    data_start = tcp_start + 16
else:
    raise RuntimeError(f"Unknown protocol: {protocol}")

payload = bytes.fromhex(data[data_start:]).decode('utf-8')

server_host = "212.182.24.27"
server_port = 2911

try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        msgA = f"zad15odpA;ver;{version};srcip;{src_ip};dstip;{dst_ip};type;{protocol}"
        s.sendto(msgA.encode('utf-8'), (server_host, server_port))
        resA, _ = s.recvfrom(4096)

        if resA:
            print(f"Server response A: {resA.decode('utf-8')}")
            if resA.decode('utf-8') == "TAK":
                msgB = f"zad15odpB;srcport;{src_port};dstport;{dst_port};data;{payload}"
                s.sendto(msgB.encode('utf-8'), (server_host, server_port))
                resB, _ = s.recvfrom(4096)

                if resB:
                    print(f"Server response B: {resB.decode('utf-8')}")
                else:
                    print("No response B from the server")
        else:
            print("No response A from the server")

except Exception as e:
    print(f"Connection error: {e}")