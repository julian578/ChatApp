from http import client
from re import A
import socket
from xmlrpc.client import Server
import threading

HEADER = 64
SERVER_PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, SERVER_PORT)

CONNECTED = True
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
USERNAME = ""

def connect_client():
    global USERNAME
    print("Type in your username")
    USERNAME = input()
    client.connect(ADDR)
    # send username to server
    send_msg(USERNAME)


def send_msg(msg):
    
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '* (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)



def handle_incoming_messages():
    
    global CONNECTED

    while  CONNECTED:
        msg_len = client.recv(HEADER).decode(FORMAT)
        if(msg_len):
            msg_len = int(msg_len)
            message = client.recv(msg_len).decode(FORMAT)
            print(message)


def handle_message_input():
           
    global CONNECTED
    while CONNECTED:

        print("type in the name of the receiving user")
        dest_username = input()
        msg = f"Hallo hier ist {USERNAME}"
        dest_user = dest_username
        send_msg(msg)
        send_msg(dest_user)
 

def start_client():
    thread = threading.Thread(target=handle_incoming_messages)
    thread.start()
    
    input_thread = threading.Thread(target=handle_message_input)
    input_thread.start()

    


connect_client()
start_client()

