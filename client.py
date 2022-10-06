import socket
import threading


HEADER = 64

FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"

#Ip address of the device the server is running on
SERVER = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5050
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (SERVER, SERVER_PORT)
CONNECTED = True
USERNAME = ""
new_messages = []


    

def connect_client():

    #global USERNAME
    #USERNAME = "Julian"
    #print("Type in your username")
    #USERNAME = input()
    client.connect(ADDR)
    start_client()
    # send username to server
    send_msg(USERNAME)
        
def start_client():
    thread = threading.Thread(target=handle_incoming_messages)
    thread.start()


def send_msg(msg):

    
    print(msg)

    message = msg.encode(FORMAT)

    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    #send_length = bytes(str(msg_length), FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def handle_incoming_messages():


    while CONNECTED:
        msg_len = client.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            message = client.recv(msg_len).decode(FORMAT)

            #check if its my own message
            mymessage = False
            if message[1:1+len(USERNAME)] == USERNAME:
                mymessage = True
            new_messages.append((message,  mymessage))




