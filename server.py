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


current_score = 0
min_score = 100000


clientsocket1,addr1 = serversocket.accept()      
print("Conexiune de la %s" % str(addr1))
clientsocket1.send(string_to_bytes(welcome_message))
clientsocket1.send(string_to_bytes(start_message))


while True:
    received_number = int.from_bytes(clientsocket1.recv(1024), "big")
    print(f'Am primit {received_number} ')

    current_score +=1
    
    if received_number == generated_number:
        clientsocket1.send(string_to_bytes(success_message))
        if min_score > current_score:
            min_score=current_score
            
        # intreaba daca vrea inca o runda
        clientsocket1.send(string_to_bytes("O noua runda? Testeaza da/nu"))
        
        # primeste raspuns
        agreement = clientsocket1.recv(1024).decode('utf-8')
        
        ##evalueaza raspunsul pt o noua runda
        # daca da => genereaza un nou nr random + continue
        if agreement.startswith("da"):
            generated_number = generate_random_number()
            current_score=0
            continue
        else:
            break
        # daca nu => break
    elif received_number < generated_number:
        clientsocket1.send(string_to_bytes(greater_than_message))
    else:
        clientsocket1.send(string_to_bytes(less_than_message))
    
    
   
clientsocket1.send(string_to_bytes('\nScorul tau maxim: ' + str(min_score)))
clientsocket1.close()

