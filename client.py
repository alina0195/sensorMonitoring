import socket

less_than_message = "Numarul este mai mic decat numarul ales"
greater_than_message = "Numarul este mai mare decat numarul ales"
success_message ="Numarul este corect"

def string_to_bytes(str):
    return bytes(str,'ascii')

def int_to_bytes(integer):
    return integer.to_bytes(2,'big')

def negative_int_to_bytes(integer):
    return integer.to_bytes(1, byteorder='big', signed=True)

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname()                           
port = 9999
clientsocket.connect((host, port))                               

wellcome_message = clientsocket.recv(1024).decode("utf-8")
print (wellcome_message)

start_message = clientsocket.recv(1024).decode("utf-8")
print (start_message)

running=True

while running:
    
    value_tried = None
    while True:
        value_tried = input(">> ")
        if value_tried.isnumeric():
            break
        else:
            print('Invalid. Introduceti un numar valid!')
            continue
    
    #ii trimite cu certitudine un numar valid 
    clientsocket.send(int_to_bytes(int(value_tried)))
    
    if running: #a introdus un numar valid
        feedback_message = clientsocket.recv(1024).decode("utf-8")
        print(feedback_message)
    
        if feedback_message.startswith(success_message):
        
            # receive question for another round
            print(clientsocket.recv(1024).decode("utf-8"))
            agreement = input(">>")
            clientsocket.send(string_to_bytes((agreement)))
            
            ## evalueaza raspunsul pt o noua runda
            if agreement=="nu":
                break
            else:
                running=True
                continue
            
        elif feedback_message==less_than_message or feedback_message==greater_than_message:
            running=True
        else:
            print("Eroare din partea serverului. Jocul se incheie...")
            break

   
print(clientsocket.recv(1024).decode("utf-8")) # scorul sau
clientsocket.close()
