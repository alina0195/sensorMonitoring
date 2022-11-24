import socket                                         
import random

welcome_message = "Bun venit! Daca doresti sa parasesti jocul tasteaza litera q."
success_message = "Numarul este corect"
less_than_message = "Numarul este mai mic decat numarul ales"
greater_than_message = "Numarul este mai mare decat numarul ales"
start_message = "Jocul a inceput. Introduce prima ta incercare "
continue_question_message = "Continui? da/nu : "

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
serversocket.listen(2) 
generated_number = generate_random_number()


numbers_of_attempts = 0
max_score = 0


clientsocket1,addr1 = serversocket.accept()      
print("Conexiune de la %s" % str(addr1))
clientsocket1.send(string_to_bytes(welcome_message))
clientsocket1.send(string_to_bytes(start_message))

while True:
    received_number = int.from_bytes(clientsocket1.recv(1024), "big")
    print(f'Am primit {received_number} ')

    numbers_of_attempts +=1
    
    if received_number == generated_number:
        clientsocket1.send(string_to_bytes(success_message))
        break
    elif received_number < generated_number:
        clientsocket1.send(string_to_bytes(greater_than_message))
    else:
        clientsocket1.send(string_to_bytes(less_than_message))
        
   
clientsocket1.send(string_to_bytes('\nScorul tau: ' + str(numbers_of_attempts)))
clientsocket1.close()

