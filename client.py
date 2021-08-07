import socket,time
import os,json
PA_Inf_FLAG = False

host = '192.168.1.150'
port = 1233

while(True):
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
        tdata = data = json.loads(os.popen('''echo '{ "command": ["get_property", "time-pos"], "request_id": 100 }' | socat - /tmp/mpvsocket''').read().strip())
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
    time.sleep(0.5)