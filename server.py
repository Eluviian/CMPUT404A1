#  coding: utf-8 
import socketserver
import socket
import threading
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

HOST, PORT = "localhost", 8080
ADDR = (HOST,PORT)

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip() #.decode('utf-8')
        print (f"Got a request from {self.client_address} of: {self.data}")
        #self.request.sendall(bytearray("OK",'utf-8'))
        #self.request.sendall(self.data.upper())
        self.data = self.data.decode('utf-8')
        
        request_list = self.data.split(' ')
        print("REQUEST LIST:",request_list)
        method = request_list[0]
        valid_path = True
        try:
            path = request_list[1] #path to what needs to be served
        except:
            valid_path = False
            self.request.sendall(bytearray('HTTP/1.1 404 Not Found!\r\n\r\n','utf-8'))
            

        if method == 'GET' and valid_path:
            #handle get request
            path = path.strip()
            #path = "www/"+path+"/index.html"

            if not path.endswith('/') and not path.endswith('css') and not path.endswith('html'):
                self.request.sendall(bytearray('HTTP/1.1 301 Moved Permanently\r\nLocation:'+path+'/'+'\r\n\r\n','utf-8'))
                print("WHYYY")
            if path.endswith('css'):
                should_be_css = True
            else:
                should_be_css = False

            if path.endswith('/') and not should_be_css:
                path += "index.html"
      
            if path.endswith('html'):
                file_type = "text/html"

            if should_be_css:
                file_type = "text/css"
                print("\nCSS\n")

            path = "www" + path
            print("PATH IS",path)
            try:
                with open(path, "r") as path_file:
                    path_data = path_file.read()
                    self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n'+"Content-Type:" + file_type +"\r\n"  +"\r\n\r\n"+path_data,'utf-8'))


            except:
                self.request.sendall(bytearray('HTTP/1.1 404 Not Found!\r\nr\n','utf-8'))

        elif valid_path:  #method other than GET
            self.request.sendall(bytearray('HTTP/1.1 405 Method Not Allowed\r\n\r\n','utf-8'))


    #def finish():   @default = nothing, this performs clean-up after handle
        #print("finsihing, cleaning up")


if __name__ == "__main__":
    

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    print("SERVER:",server)
    print("HOST:",HOST)
    print("PORT",PORT)
    print("MYWEBSERVER:",MyWebServer)


    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


'''
#https://www.youtube.com/watch?v=3QiPPX-KeSc&feature=youtu.be
#Tech with Tim  https://www.youtube.com/@TechWithTim

import socketserver
import socket
import threading
PORT = 8080 #HTTP port
SERVER = socket.gethostbyname(socket.gethostname())  #gets ip address of device hosting server
ADDR = (SERVER, PORT)  #address needs to be in a tuple
HEADER = 64  #specifying that first message to the server needs to be a header of length 64, will be a number which represents length of message to be recieved
FORMAT = 'utf-8'
DISCONNECT_MSG = "[DISCONNECT]"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #using internet, stremaing data
server.bind(ADDR)  #socket is now for this specific server/port

def handle_client(conn, addr):
    #running concurrently for each client
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:   #waiting for messages from client

        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MSG:
                connected = False

            print(f"[addr]: {ADDR}: {msg}")
            conn.send("MSG received".encode(FORMAT))

def start():
    #handles new connections, distributes them

    server.listen()  #listening for new connections
    print(f"[LISTENING] Server is listening on {SERVER}")
    
    while True:  #infinite loop
        conn, addr = server.accept() #waits for new connection to server, records conn (socket object), and addr (ip and port)
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")  #number of threads = number of clients + 1 start thread

print("[STARTING] server is starting...")
start()
'''