import socket
# https://www.bogotobogo.com/python/python_network_programming_server_client.php

def string_to_bytes(str):
    return bytes(str,'ascii')

def int_to_bytes(integer):
    return integer.to_bytes(2,'big')

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname()                           
port = 9999
clientsocket.connect((host, port))                               

wellcome_message = clientsocket.recv(1024).decode("utf-8")
print (wellcome_message)

start_message = clientsocket.recv(1024).decode("utf-8")
print (start_message)


less_than_message = "Numarul este mai mic decat numarul ales"
greater_than_message = "Numarul este mai mare decat numarul ales"
success_message ="Numarul este corect"


while True:
    value_tried = input(">> ")
    clientsocket.send(int_to_bytes(int(value_tried)))
    
    feedback_message = clientsocket.recv(1024).decode("utf-8")
    print(feedback_message)
    
    if feedback_message.startswith(success_message):
        break
    elif feedback_message==less_than_message or feedback_message==greater_than_message:
        continue
    else:
        print("Eroare din partea serverului. Jocul se incheie...")
        break
        

clientsocket.close()
