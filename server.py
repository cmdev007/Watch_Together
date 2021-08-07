import socket
import os
from _thread import *

all_cli = set()

ServerSocket = socket.socket()
ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    while True:
        data = connection.recv(2048)
        if not data:
            break
        if "PAUSE" in data.decode('utf-8').strip():
            send_all("PA")
        elif "PLAY" in data.decode('utf-8').strip():
            send_all("PL")
    connection.close()

def send_all(msg):
    for i in all_cli:
        try:
            i.send(str.encode(msg+"\r\n"))
        except:
            pass

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    all_cli.add(Client)
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()