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

while True:
    Input = input('Your guess: ')
    ClientSocket.send(str.encode(Input))
    if Input=='BYE':
        break
    res = ClientSocket.recv(1024).decode('utf-8')
    print(res)
    if res.startswith('Felicitaari'):
        break

print(ClientSocket.recv(1024).decode('utf-8')) #scorul il primeste la final
ClientSocket.close()