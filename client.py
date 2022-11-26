import socket
import sys
less_than_message = "Numarul este mai mic decat numarul ales"
greater_than_message = "Numarul este mai mare decat numarul ales"
success_message ="Numarul este corect"

def string_to_bytes(str):
    return bytes(str,'ascii')

def int_to_bytes(integer):
    return integer.to_bytes(2,'big')

def negative_int_to_bytes(integer):
    return integer.to_bytes(1, byteorder='big', signed=True)


try:
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
except socket.error as e:
    print ("Error creating socket: %s" % e)
    sys.exit(1)

try:
    host = socket.gethostname()                           
    port = 9999
    clientsocket.connect((host, port))   
except socket.gaierror as e:
    print ("Address-related error connecting to server: %s" % e) 
    sys.exit(1)
except socket.error as e: 
    print ("Connection error: %s" % e) 
    sys.exit(1)                  


try:
    wellcome_message = clientsocket.recv(1024).decode("utf-8")
    print (wellcome_message)
except socket.error as e: 
    print (f'Error receiving data: {e}') 
    sys.exit(1)

try:
    start_message = clientsocket.recv(1024).decode("utf-8")
    print (start_message)
except socket.error as e: 
    print (f'Error receiving data: {e}') 
    sys.exit(1)

running=True

try:
    while running:
        
        value_tried = None
        while True:
            value_tried = input(">> ")
            if value_tried.isnumeric():
                break
            elif value_tried.lower().strip()=='q':
                print('Parasire joc...')
                running=False
                break
            else:
                print('Invalid. Introduceti un numar valid sau parasiti jocul (q)!')
                continue
        
        #ii trimite cu certitudine un numar valid 
        clientsocket.send(str(value_tried).encode('utf-8'))
        
        if running: #a introdus un numar valid
            feedback_message = clientsocket.recv(1024).decode("utf-8")
            print(feedback_message)
        
            if feedback_message.startswith(success_message):
            
                # receive question for another round
                print(clientsocket.recv(1024).decode("utf-8"))
                agreement = None
                while True:
                    agreement = input(">>")
                    if agreement.lower().strip()=="nu" or agreement.lower().strip()=="da":
                        break
                    else:
                        print("Raspuns invalid")
                        continue
                clientsocket.send(string_to_bytes((agreement)))
                
                ## evalueaza raspunsul pt o noua runda
                if agreement.lower().strip()=="nu":
                    break
                elif agreement.lower().strip()=="da":
                    running=True
                    continue
                
            elif feedback_message==less_than_message or feedback_message==greater_than_message:
                running=True
            else:
                print("Eroare din partea serverului. Jocul se incheie...")
                break

    print(clientsocket.recv(1024).decode("utf-8")) # scorul sau
except socket.error as e:
    print(f'Erori in comunicarea cu serverul')
finally:
    clientsocket.close()
