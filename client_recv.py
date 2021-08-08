#!/usr/bin/env python3

import socket,os

HOST = '52.149.146.58'  # The server's hostname or IP address
PORT = 1233        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
    while True:
        data = s.recv(1024)
        if data:
            data = data.decode('utf-8')
            print(data)
        else:
            break
        if "PL" in data:
            os.system('''echo '{ "command": ["set_property", "pause", false] }' | socat - /tmp/mpvsocket''')
        elif "PA" in data:
            os.system('''echo '{ "command": ["set_property", "pause", true] }' | socat - /tmp/mpvsocket''')
            SEEK = float(data.split("|")[-1])
            os.system('''echo '{ "command": ["set_property", "time-pos", "''' + str(SEEK) + '''"], "request_id": 100 }' | socat - /tmp/mpvsocket''')
        elif "SA" in data:
            SEEK = float(data.split("|")[-1])
            os.system('''echo '{ "command": ["set_property", "time-pos", "''' + str(SEEK) + '''"], "request_id": 100 }' | socat - /tmp/mpvsocket''')