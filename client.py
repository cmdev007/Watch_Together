import socket,time
import os,json
from _thread import start_new_thread
import argparse

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-c', action='store_true')
args = my_parser.parse_args()

if args.c:
    CFLAG = True

PA_Inf_FLAG = False
SEEK_FLAG = True
host = '52.149.146.58'
port = 1233

def actioner():
    global SEEK_FLAG
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
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
                # SEEK = float(data.split("|")[-1])
                # os.system('''echo '{ "command": ["set_property", "time-pos", "''' + str(SEEK) + '''"], "request_id": 100 }' | socat - /tmp/mpvsocket''')
            elif "SA" in data:
                SEEK = float(data.split("|")[-1])
                os.system('''echo '{ "command": ["set_property", "time-pos", "''' + str(SEEK) + '''"], "request_id": 100 }' | socat - /tmp/mpvsocket''')
                SEEK_FLAG = False

start_new_thread(actioner,())

TIME = 0
S_Counter = 0
while(True):
    Old_Time = TIME
    #Realtime time sync
    try:
        tdata = json.loads(os.popen('''echo '{ "command": ["get_property", "time-pos"], "request_id": 100 }' | socat - /tmp/mpvsocket''').read().strip())
        TIME = tdata['data']
    except:
        pass
    if abs(TIME-Old_Time) > 2 and SEEK_FLAG:
        ClientSocket = socket.socket()

        print('Waiting for connection')
        try:
            ClientSocket.connect((host, port))
        except socket.error as e:
            print(str(e))
        try:
            Input = "SEEK"
            tdata = json.loads(os.popen('''echo '{ "command": ["get_property", "time-pos"], "request_id": 100 }' | socat - /tmp/mpvsocket''').read().strip())
            SEEK = tdata['data']
            ClientSocket.send(str.encode(f"{Input}|{SEEK}"))
        except:
            pass
        ClientSocket.close()

    PSTATE = True
    try:
        data = json.loads(os.popen('''echo '{ "command": ["get_property", "pause"] }' | socat - /tmp/mpvsocket''').read().strip())
        PSTATE = data['data']
    except:
        print("Something is wrong!")
    if PSTATE and not PA_Inf_FLAG:
        ClientSocket = socket.socket()

        print('Waiting for connection')
        try:
            ClientSocket.connect((host, port))
        except socket.error as e:
            print(str(e))

        Input = "PAUSE"
        try:
            tdata = json.loads(os.popen('''echo '{ "command": ["get_property", "time-pos"], "request_id": 100 }' | socat - /tmp/mpvsocket''').read().strip())
            SEEK = tdata['data']
            ClientSocket.send(str.encode(f"{Input}|{SEEK}"))
            Response = ClientSocket.recv(1024)
            print(Response.decode('utf-8'))
        except:
            pass
        
        ClientSocket.close()
        PA_Inf_FLAG = True

    elif not PSTATE and PA_Inf_FLAG:
        ClientSocket = socket.socket()

        print('Waiting for connection')
        try:
            ClientSocket.connect((host, port))
        except socket.error as e:
            print(str(e))

        Input = "PLAY"
        ClientSocket.send(str.encode(Input))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))

        ClientSocket.close()
        PA_Inf_FLAG = False
    
    if not SEEK_FLAG:
        if S_Counter < 4:
            S_Counter+=1
        else:
            S_Counter = 0
            SEEK_FLAG = True

    if PSTATE and SEEK_FLAG:
        time.sleep(0.1)
    else:
        time.sleep(0.5)