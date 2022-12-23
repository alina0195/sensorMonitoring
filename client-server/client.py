import urllib.request
import json
from guizero import App, Text, TextBox, Combo, PushButton, Box,info
from time import sleep
import threading
import requests

#TO DO : de adaugat last_valid_limits (la schimbarea senzorului din casuta cand sunt setate valori min-max anterioare nu mai merge bine)
limits={
    'presiune': {"min":1,"max":30},
    'tensiune': {'min':190,"max":280},
    'curent': {'min':0,'max':800}
}

maxVal = -1
minVal = -1


currentValue = -1
stopThreadEventRaised = False
address = ''
port = ''
senzor = 'presiune'
status = 'OFF'


def startServer():
    startButton.disable()
    stopButton.enable()
    global pollServerThread
    global address, port
    address= address_textbox.value
    port = port_textbox.value
    if address =='':
        info('Adress Error','Address field must be filled with a value.')
        return
    if int(port)>65535 or int(port)<0 or port=='':
        info('Port Error','Port number must be between 0 and 65535.')
        return
    
    if address != '127.0.0.1' or port != '60000':
        info('Error',  'Adress or port number is not correct!\n The server is running on 127.0.0.1:60000')
    else:
        print(f'Connecting to server on https://{address}:{port}')
        pollServerThread = threading.Thread(target=connect_to_server, args=(address,port))
        pollServerThread.start()


def stopPollingServer():
    startButton.enable()
    stopButton.disable()
    print("In stop polling server")
    global stopThreadEventRaised
    stopThreadEventRaised = True
    status_textbox.value='OFF'
    
    
def connect_to_server(address,port):
    global curent, tensiune, presiune
    global stopThreadEventRaised
    global currentValue, senzor, limits, status
    
    stopThreadEventRaised = False

    url = 'http://'+address+':'+port
    
    while not stopThreadEventRaised:
        print("Stop thread event raised value is ", stopThreadEventRaised)
        json_url=urllib.request.urlopen(url)
        response = json.loads(json_url.read().decode('utf-8'))
        if response:
            status='ON'
        else:
            status='OFF'
        curent = response['Curent']
        tensiune = response['Tensiune']
        presiune = response['Presiune']
        print('Informatia primita de la server:\n', 'Curent:=',curent,'Tensiune=',tensiune,'Presiune=',presiune)
        status_textbox.value=status

        print('Senzor=', senzor)
        if senzor.lower()=='presiune':
            currentValue=presiune
        elif senzor.lower()=='curent':
            currentValue=curent
        elif senzor.lower()=='tensiune':
            currentValue=tensiune
        text_current_value.value=f'Valoare curenta pentru {senzor}:{currentValue}'
        
        if minVal!=-1 and maxVal!=-1:
            if int(minVal)> int(currentValue) or int(maxVal)< int(currentValue):
                info('Error','Eroare valoare monitorizata!')
                text_current_value.value = f'Eroare valoare pentru {senzor}'
            

        sleep(5)
   
   
def minValChanged(event):
    global minVal
    if event.key == "\r":
        print("Min val has changed")
        minVal = val_min_textbox.value
        if maxVal != -1:
            if int(minVal)>int(maxVal):
                info('Error','Valoare minima invalida')
            else:
                postSetMinMaxReq()
    
    
def maxValChanged(event):
    global maxVal
    if event.key == "\r":
        maxVal = val_max_textbox.value
        print("Max val has changed")
        if minVal != -1:
            if int(maxVal) < int(minVal):
                info('Error','Valoare maxima invalida')
            else:    
                postSetMinMaxReq()


def postSetMinMaxReq():
    global address, port, senzor
    if address and port and senzor:    
        url = 'http://'+address+':'+port+"/minmax"
        payload = {"senzorName":senzor, "minVal":minVal,"maxVal":maxVal}
        requests.post(url, json=payload)


def senzorNameSelected(event):
    global currentValue, senzor
    global curent, presiune, tensiune
    if event.key == "\r":
        senzor = senzor_textbox.value
        if len(senzor)<=3:
            info('Error','Numele senzorului trebuie sa contina cel putin 3 caractere')
        else:
            senzor = senzor_textbox.value
            if senzor.lower()=='presiune':
                currentValue=presiune
            elif senzor.lower()=='curent':
                currentValue=curent
            elif senzor.lower()=='tensiune':
                currentValue=tensiune
            else:
                info('Eroare','Nume de senzor invalid. Incercati: presiune/curent/tensiune.')
            text_current_value.value=f'Valoare curenta pentru {senzor}:{currentValue}'
 
 
app = App(title="Proiect")
Text(app,text="Proiect")

form = Box(app, width="fill", layout="grid")
form.border = True

Text(form, text="Adresa:", grid=[0,0], align="right")
address_textbox = TextBox(form, grid=[1,0],width=40)

Text(form, text="Port:", grid=[0,1], align="right")
port_textbox = TextBox(form, grid=[1,1],width=40)

Text(form, text="Senzor:", grid=[0,2], align="right")
senzor_textbox = TextBox(form, grid=[1,2],width=40)
senzor_textbox.when_key_pressed = senzorNameSelected

#TO DO: check valid intervals min<max
Text(form, text="Val min:", grid=[0,3], align="right")
val_min_textbox =TextBox(form, grid=[1,3], width=40)
val_min_textbox.when_key_pressed = minValChanged

Text(form, text="Val max:", grid=[0,4], align="right")
val_max_textbox = TextBox(form, grid=[1,4], width=40)
val_max_textbox.when_key_pressed = maxValChanged

Text(form, text="Sistem:", grid=[0,5], align="right")
status_textbox = Text(form, text=status, grid=[1,5])

#TO DO: add value error as text
text_current_value = Text(app, text=f"Valoare curenta pentru {senzor}:{currentValue}")

form_buttons = Box(app,  layout="grid")
# TO DO: change text of the button on toggle between them
startButton = PushButton(form_buttons, command=startServer, text="Start", grid=[0,0])
stopButton = PushButton(form_buttons, command=stopPollingServer, text="Stop", grid=[1,0])

app.display()