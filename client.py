import socket,time
import os,json
PA_Inf_FLAG = False
while(True):
    PSTATE = True
    try:
        data = json.loads(os.popen('''echo '{ "command": ["get_property", "pause"] }' | socat - /tmp/mpvsocket''').read().strip())
        PSTATE = data['data']
    except:
        print("Something is wrong!")
    if PSTATE and not PA_Inf_FLAG:
        ClientSocket = socket.socket()
        host = '127.0.0.1'
        port = 1233

        print('Waiting for connection')
        try:
            ClientSocket.connect((host, port))
        except socket.error as e:
            print(str(e))

        Input = "PAUSE"
        ClientSocket.send(str.encode(Input))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))

        ClientSocket.close()
        PA_Inf_FLAG = True
    elif not PSTATE and PA_Inf_FLAG:
        ClientSocket = socket.socket()
        host = '127.0.0.1'
        port = 1233

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