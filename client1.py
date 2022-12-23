import socket

host = '127.0.0.1'
port = 9999
success_message = "Numarul este corect"
less_than_message = "Numarul este mai mic decat numarul ales"
greater_than_message = "Numarul este mai mare decat numarul ales"


ClientSocket = socket.socket()
print('Asptept sa ma conectez')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))


print(ClientSocket.recv(1024).decode('utf-8')) #welcome message

running=True

while running:
    Input = None
    while True: #validare input
        Input = input('>> ')
        if Input.isnumeric():
            break
        elif Input=='q':
            running=False
            break
        else:
            print("Invalid.Introduceti un numar sau parasiti jocul.")
        
    ClientSocket.send(str.encode(Input))
    
    if running:
        feedback = ClientSocket.recv(1024).decode('utf-8')
        print(feedback)
        
        if feedback==success_message:
            print(ClientSocket.recv(1024).decode('utf-8')) # continui?da/nu
            agreement = input(">>")
            ClientSocket.send(str.encode(agreement))
            if agreement=="da":
                running=True
                continue
            elif agreement=="nu":
                break
        elif feedback==less_than_message or feedback==greater_than_message:
            continue
        else:
            print("Eroare din partea serverului. Jocul se incheie...")
            break

print(ClientSocket.recv(1024).decode('utf-8')) #scorul il primeste la final
ClientSocket.close()