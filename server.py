import socket
import random


host = '127.0.0.1'
port = 9999
MAX_VAL = 100000

welcome_message = "Bun venit! Daca doresti sa parasesti jocul tasteaza litera q.\nIncearca sa ghicesti numarul:"
success_message = "Numarul este corect"
less_than_message = "Numarul este mai mic decat numarul ales"
greater_than_message = "Numarul este mai mare decat numarul ales"
start_message = "Jocul a inceput. Introduce prima ta incercare "
continue_question_message = "Continui? da/nu"


def int_to_bytes(integer):
    return integer.to_bytes(2,'big')

def generate_random_number():
    nb = random.randint(0,50)
    print(f'Am generat: {nb}')
    return nb


def client1_handler_2players(connection,nr, adv_conn):
    connection.send(str.encode(welcome_message))
    current_score = 0
    min_score = MAX_VAL
    while True:
        res = connection.recv(1024).decode('utf-8')
        if res =='q':
            adv_conn.send(str.encode(res))
            if min_score==MAX_VAL:
                min_score=0 # e prima runda si doreste sa paraseasca jocul
            break
        
        current_score +=1
        if res == str(nr):
            connection.send(str.encode(success_message))
            adv_conn.send(str.encode(success_message))
            
            if current_score < min_score:
                min_score=current_score
            connection.send(str.encode(continue_question_message))
            agreement = connection.recv(1024).decode('utf-8')
            adv_conn.send(str.encode(agreement))
            
            if agreement=="da":
                current_score=0
                nr = int(adv_conn.recv(1024).decode('utf-8'))
                continue
            else: 
                break
        elif int(res)<nr:
            connection.send(str.encode(greater_than_message))
            adv_conn.send(str.encode(greater_than_message))
            
        elif int(res)>nr:
            connection.send(str.encode(less_than_message))
            adv_conn.send(str.encode(less_than_message))
            
    return min_score  


def client1_handler_1player(connection,nr):
    connection.send(str.encode(welcome_message))
    current_score = 0
    min_score = MAX_VAL
    while True:
        res = connection.recv(1024).decode('utf-8')
        if res =='q':
            if min_score==MAX_VAL:
                min_score=0 # e prima runda si doreste sa paraseasca jocul
            break
        
        current_score +=1
        if res == str(nr):
            connection.send(str.encode(success_message))
            if current_score < min_score:
                min_score=current_score
            connection.send(str.encode(continue_question_message))
            agreement = connection.recv(1024).decode('utf-8')
            if agreement.startswith("da"):
                current_score=0
                nr = generate_random_number()
                continue
            else: 
                break

        elif int(res)<nr:
            connection.send(str.encode(greater_than_message))
        elif int(res)>nr:
            connection.send(str.encode(less_than_message))
    
    return min_score    


def client2_handler(connection):
    connection.send(str.encode(welcome_message))
    nr = int(connection.recv(1024).decode('utf-8'))
    return nr


def accept_one_connection(ServerSocket):
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    generated_number = generate_random_number()
    min_score = client1_handler_1player(Client, generated_number)
    Client.send(str.encode('Scor maxim: '+str(min_score)))
    Client.close()


def accept_two_connections(ServerSocket):
    Client1, address1 = ServerSocket.accept()
    print('Connected to: ' + address1[0] + ':' + str(address1[1]))
    Client2, address2 = ServerSocket.accept()
    print('Connected to: ' + address2[0] + ':' + str(address2[1]))
    nr = client2_handler(Client2)
    min_score = client1_handler_2players(Client1,nr, Client2)
    Client1.send(str.encode('Scor: '+str(min_score)))
    Client2.send(str.encode('Scor: '+str(min_score)))
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
    option = input("Type number of players[1 or 2]\n>>")
    if option=='1':
        accept_one_connection(ServerSocket)
    elif option=='2':
        accept_two_connections(ServerSocket)

start_server(host, port)