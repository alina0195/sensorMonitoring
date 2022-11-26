import socket                                         
import random
import sys

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

try:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
except socket.error as e:
     print ("Error creating socket: %s" % e)
     sys.exit(1)

try:
    host = socket.gethostname() 
    port = 9999                                           
    serversocket.bind((host, port)) 
except socket.gaierror as e:
    print ("Address-related error connecting to server: %s" % e) 
    sys.exit(1)
except socket.error as e: 
    print ("Connection error: %s" % e) 
    sys.exit(1) 
    
serversocket.listen(2) 
generated_number = generate_random_number()

MAX_VAL = 100000
current_score = 0
min_score = MAX_VAL


clientsocket1,addr1 = serversocket.accept()      
print("Conexiune de la %s" % str(addr1))

try:
    clientsocket1.send(string_to_bytes(welcome_message))
except socket.error as e: 
    print (f'Error sending data: {e}') 
    sys.exit(1)
try:
    clientsocket1.send(string_to_bytes(start_message))
except socket.error as e: 
    print (f'Error sending data: {e}') 
    sys.exit(1)

try:
    while True:
        try:
            received = clientsocket1.recv(1024).decode('utf-8')
            if str(received).lower().strip().startswith('q'):
                print("Clientul a parasit jocul")
                if min_score==MAX_VAL:
                    min_score=0
                break
            else:
                received_number = int(received)
                print(f'Am primit {received_number} ')
        except socket.error as e:
            print(f'Error receiving data: {e}')

        current_score +=1
        
        if received_number == generated_number:
            clientsocket1.send(string_to_bytes(success_message))
            if current_score < min_score:
                min_score=current_score
            # intreaba daca vrea inca o runda
            clientsocket1.send(string_to_bytes("O noua runda? da/nu"))
            
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
    
except socket.error as e:
    print(f'Erori in comunicarea cu clientul')
finally:
    clientsocket1.close()

