from curses import COLOR_WHITE
from http import client
from re import A
import socket
from xmlrpc.client import Server
import threading
import pygame



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
        print("Type in your username")
        USERNAME = input()
        client.connect(self.ADDR)
        # send username to server
        self.send_msg(USERNAME)


    def send_msg(msg, self):

        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b" " * (self.HEADER - len(send_length))
        client.send(send_length)
        client.send(message)


    def handle_incoming_messages(self):


        while self.CONNECTED:
            msg_len = client.recv(self.HEADER).decode(self.FORMAT)
            if msg_len:
                msg_len = int(msg_len)
                message = client.recv(msg_len).decode(self.FORMAT)
                print(message)


    def handle_message_input(self):

        
        while self.CONNECTED:

            print("type in the name of the receiving user")
            dest_username = input()
            msg = f"Hallo hier ist {USERNAME}"
            dest_user = dest_username
            self.send_msg(msg)
            self.send_msg(dest_user)


    def start_client(self):
        thread = threading.Thread(target=self.handle_incoming_messages)
        thread.start()

        input_thread = threading.Thread(target=self.handle_message_input)
        input_thread.start()

