import socket
import random
host = '127.0.0.1'
port = 9999
success_message = "Numarul este corect"


def generate_random_number():
    nb = random.randint(0,50)
    print(f'Am generat: {nb}')
    return nb

ClientSocket = socket.socket()
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

print(ClientSocket.recv(1024).decode('utf-8'))
nr = generate_random_number()
ClientSocket.send(str.encode(str(nr))) # trimite nr generat random

while True:
    feedback = ClientSocket.recv(1024).decode('utf-8')
    print(feedback)
    if feedback=='q':
        break
    if feedback==success_message:
        agreement = ClientSocket.recv(1024).decode('utf-8')
        if agreement=='da':
            nr=generate_random_number()
            ClientSocket.send(str.encode(str(nr))) # trimite nr generat random
        else:
            break
    
print(ClientSocket.recv(1024).decode('utf-8')) # la final primeste scorul
ClientSocket.close()