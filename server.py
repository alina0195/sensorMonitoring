import socket                                         
import time
import random

def string_to_bytes(str):
    return bytes(str,'ascii')

def int_to_bytes(integer):
    return integer.to_bytes(2,'big')

def generate_random_number():
    nb = random.randint(0,50)
    print(f'Am generat: {nb}')
    return nb


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname() 
port = 9999                                           
serversocket.bind((host, port))  
serversocket.listen(5) 

welcome_message = "Bun venit!"
success_message = "Numarul este corect"
less_than_message = "Numarul este mai mic decat numarul ales"
greater_than_message = "Numarul este mai mare decat numarul ales"
start_message = "Jocul a inceput. Introduce prima ta incercare "

clientsockets = []
numbers_of_attempts = [0]*2
client_index=-1
max_score = 0

while True:
    clientsocket,addr = serversocket.accept()      
    clientsockets.append(clientsocket)
    client_index+=1
    
    print("Conexiune de la %s" % str(addr))
    
    clientsocket.send(string_to_bytes(welcome_message))
    
    generated_number = generate_random_number()
    clientsocket.send(string_to_bytes(start_message))
    
    while True:
        received_number = int.from_bytes(clientsocket.recv(1024), "big")
        print(f'Am primit {received_number} ')
        if received_number == generated_number:
            success_message += '\nScorul tau: ' + str(numbers_of_attempts[client_index])
            clientsocket.send(string_to_bytes(success_message))
            break
        elif received_number < generated_number:
            clientsocket.send(string_to_bytes(greater_than_message))
            numbers_of_attempts[client_index] +=1
        else:
            clientsocket.send(string_to_bytes(less_than_message))
            numbers_of_attempts[client_index] +=1
                
    break 

for client in clientsockets:
    client.close()

