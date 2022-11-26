# Imports
import socket
from _thread import *

# https://stackoverflow.com/questions/27139240/i-need-the-server-to-send-messages-to-all-clients-python-sockets
# https://github.com/mittalmehul/socket-server/blob/master/client.py 

host = '127.0.0.1'
port = 1233

def client_handler1_2players(connection, nr, adv_conn):
    scor = 0
    connection.send(str.encode('You are now connected to the replay server... Type BYE to stop'))
    while True:
        res = connection.recv(2048).decode('utf-8')
        if res == str(nr):
            connection.send(str.encode("Felicitaari"))
            adv_conn.send(str.encode("Felicitaari"))
            break
        elif res =='BYE':
            adv_conn.send(str.encode("BYE"))
            break
        else:
            # trimite notificare catre client 
            connection.send(str.encode("E mai mare sau mai mic"))
            adv_conn.send(str.encode("E mai mare sau mai mic"))
        scor += 1
    return scor


def client_handler1_1player(connection,nr):
    scor = 0
    connection.send(str.encode('You are now connected to the replay server... Type BYE to stop'))
    while True:
        res = connection.recv(2048).decode('utf-8')
        if res == str(nr):
            connection.send(str.encode("Felicitaari"))
            break
        elif res =='BYE':
            break
        else:
            # trimite notificare catre client 
            connection.send(str.encode("E mai mare sau mai mic"))
        scor += 1
    return scor


def client_handler2(connection):
    connection.send(str.encode('You are now connected to the replay server...'))
    nr = int(connection.recv(1024).decode('utf-8'))
    return nr


def accept_one_connection(ServerSocket):
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    scor = client_handler1_1player(Client, 20)
    Client.send(str.encode('Scor: '+str(scor)))
    Client.close()


def accept_two_connections(ServerSocket):
    Client1, address1 = ServerSocket.accept()
    print('Connected to: ' + address1[0] + ':' + str(address1[1]))
    Client2, address2 = ServerSocket.accept()
    print('Connected to: ' + address2[0] + ':' + str(address2[1]))
    nr = client_handler2(Client2)
    scor = client_handler1_2players(Client1,nr, Client2)
    Client1.send(str.encode('Scor: '+str(scor)))
    Client2.send(str.encode('Scor: '+str(scor)))
    Client2.close()
    Client1.close()
    

def start_server(host, port):
    ServerSocket = socket.socket()
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print(f'Server is listing on the port {port}...')
    ServerSocket.listen(2)
    option = input("Type number of players\n>>")
    if option=='1':
        accept_one_connection(ServerSocket)
    elif option=='2':
        accept_two_connections(ServerSocket)

start_server(host, port)