
import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"


#dictonary conn:username
connected_users = {}


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {connected_users[conn]} connected")
    connected = True
    
    while(connected):
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
        
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            msg = f"[{connected_users[conn]}] " + msg
            print(msg)

            if msg == DISCONNECT_MESSAGE:
                disconnect_user(conn)
                connected = False

            #send the message to all connected users
            for key in connected_users:
                if key != conn:
                    send_msg(key, msg)
        

    
    conn.close()


def disconnect_user(conn):
    print(f"[{connected_users[conn]}] disconnected")
    del connected_users[conn]


def send_msg(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    conn.send(send_length)
    conn.send(message)


#returns the username of a new connection
def get_username(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        
        return msg
    

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        
        username = get_username(conn)
        
        connected_users[conn] = username

        print(connected_users)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"ACTIVE CONNECTIONS: {threading.activeCount() -1} ")



print(f"SERVER is starting on port {PORT}")
start()