import socket,time
import os,json
PA_Inf_FLAG = False

host = '52.149.146.58'
port = 1233
TIME = 0
while(True):
    Old_Time = TIME
    #Realtime time sync
    tdata = json.loads(os.popen('''echo '{ "command": ["get_property", "time-pos"], "request_id": 100 }' | socat - /tmp/mpvsocket''').read().strip())
    TIME = tdata['data']
    if abs(TIME-Old_Time) > 2:
        ClientSocket = socket.socket()

        print('Waiting for connection')
        try:
            ClientSocket.connect((host, port))
        except socket.error as e:
            print(str(e))

        Input = "SEEK"
        tdata = json.loads(os.popen('''echo '{ "command": ["get_property", "time-pos"], "request_id": 100 }' | socat - /tmp/mpvsocket''').read().strip())
        SEEK = tdata['data']
        ClientSocket.send(str.encode(f"{Input}|{SEEK}"))
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
        tdata = json.loads(os.popen('''echo '{ "command": ["get_property", "time-pos"], "request_id": 100 }' | socat - /tmp/mpvsocket''').read().strip())
        SEEK = tdata['data']
        ClientSocket.send(str.encode(f"{Input}|{SEEK}"))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
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
    if not PSTATE:
        time.sleep(0.5)