#https://www.youtube.com/watch?v=3QiPPX-KeSc&feature=youtu.be
#Tech with Tim  https://www.youtube.com/@TechWithTim
''''''
import socket

HEADER = 64
PORT = 8080
FORMAT = 'utf-8'
DISCONNECT_MSG = "[DISCONNECT]"


SERVER = "localhost"
ADDR = (SERVER, PORT)



def send(msg):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    message = msg.encode(FORMAT)
    # msg_length = len(message)
    # send_length = str(msg_length).encode(FORMAT)
    # send_length += b' ' * (HEADER-len(send_length))  #pad so it is length 64
    # client.send(send_length) #HEADER
    client.send(message)
    resp = client.recv(2048).decode(FORMAT) #message from server "Message Receieved"
    while len(resp) > 0:
        print(resp)
        resp = client.recv(2048)

    client.close()


send("GET www/index.html")
with open("www/index.html", "r") as path_file:
    path_data = path_file.read()
    print(path_data)


