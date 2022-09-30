from curses import COLOR_WHITE
from re import A
import socket
from xmlrpc.client import Server
import threading




class Client():
    def __init__(self):

        self.HEADER = 64
        self.SERVER_PORT = 5050
        self.FORMAT = "utf-8"
        self.DISCONNECT_MESSAGE = "!disconnect"
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.SERVER_PORT)
        self.CONNECTED = True
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.USERNAME = ""
        

    def connect_client(self):

        global USERNAME
        USERNAME = "Julian"
        #print("Type in your username")
        #USERNAME = input()
        self.client.connect(self.ADDR)
        print("user connected")
        self.start_client()
        # send username to server
        #self.send_msg(USERNAME)
        
    def start_client(self):
        thread = threading.Thread(target=self.handle_incoming_messages)
        thread.start()


    def send_msg(msg, self):

        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b" " * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)


    def handle_incoming_messages(self):


        while self.CONNECTED:
            msg_len = self.client.recv(self.HEADER).decode(self.FORMAT)
            if msg_len:
                msg_len = int(msg_len)
                message = self.client.recv(msg_len).decode(self.FORMAT)
                print(message)



    

Client()