import socket

host = '127.0.0.1'
port = 1233


ClientSocket = socket.socket()
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

message = ClientSocket.recv(1024)
print(message)

ClientSocket.send(str.encode('10')) # trimite nr generat random

while True:
    decizie = ClientSocket.recv(1024).decode('utf-8')
    print(decizie)
    if decizie=='BYE' or decizie.startswith('Felicitaari'):
        break
    
print(ClientSocket.recv(1024).decode('utf-8')) # la final primeste scorul
ClientSocket.close()