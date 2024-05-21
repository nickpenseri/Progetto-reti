# -*- coding: utf-8 -*-
"""
Created on Mon May 20 11:54:31 2024

@author: nickp
"""

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import tkinter as tkt

#funzione per ricevere i messaggi, che verrà invocata 
#in un thread sempre attivo dall'inizio della connessione
def ricevi_messaggi():
    while True:
        try:
            #ricezione dei messaggi in arrivo sul socket
            messaggio=client_socket.recv(BUFSIZE).decode("utf8")
            #inserimento del messaggio nella lista dei messaggi visualizzati nella finestra
            lista_messaggi.insert(tkt.END, messaggio)
            
        #se ci sono eccezioni dovute all'abbandono della chat non si attendono più nuovi messaggi
        except OSError:
            break
        

#funzione per inviare messaggi, chiamata al momento della pressione del pulsante invio
def invio(event = None):
    #lettura del messaggio da inviare dalla casella di invio e liberazione della casella
    messaggio=my_msg.get()
    my_msg.set("")
    #invio del messaggio sul socket
    client_socket.send(bytes(messaggio, "utf8"))
    #se il messaggio è quello con cui si termina la connessione si attende l'ultimo messaggio mandato dal server
    #e si chiudono il socket e la finestra
    if messaggio == "{quit}":
        client_socket.recv(BUFSIZE)
        client_socket.close()
        finestra.destroy()
        
#funzione che viene chiamata al momento della chiusura della finestra che chiude anche il socket
def chiusura(event = None):
    my_msg.set("{quit}")
    invio()
    
#creazione della finestra e impostazione del titolo
finestra = tkt.Tk()
finestra.title("Chat client-server")

#creazione del frame per contenere i messaggi
messages_frame = tkt.Frame(finestra)
#stringa per memorizzare i messaggi da inviare
my_msg = tkt.StringVar()
#indicazione della casella per inviare i messaggi
my_msg.set("Scrivi qui i tuoi messaggi.")
#scrollbar per navigare nei messaggi precedenti
scrollbar = tkt.Scrollbar(messages_frame)

#creazione della lista per contenere i messaggi in arrivo
lista_messaggi = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
lista_messaggi.pack(side=tkt.LEFT, fill=tkt.BOTH)
lista_messaggi.pack()
messages_frame.pack()

#Creazione del campo di input e associazione alla variabile stringa
entry_field = tkt.Entry(finestra, textvariable=my_msg)
#collegamento della funzione invio al tasto Return
entry_field.bind("<Return>", invio)

entry_field.pack()
#creazione del pulsante invio e associazione alla funzione invio
send_button = tkt.Button(finestra, text="Invio", command=invio)
#integrazione del tasto nel pacchetto
send_button.pack()

#associazione della funzione chiusura alla chiusura della finestra
finestra.protocol("WM_DELETE_WINDOW", chiusura)


#richiesta di inserimento della coppia indirizzo-porta del server
#se non viene specificato uno dei due vengono chiesti nuovamente
while True: 
    INDIRIZZO_SERVER=input("Inserire l'indirizzo IP del server host: ")
    PORTA_SERVER=input("Inserire la porta del server host: ")
    if not INDIRIZZO_SERVER or not PORTA_SERVER:
        print("Indirizzo non valido, inserire nuovamente")
    else:
        break

#numero massimo di byte da ricevere
BUFSIZE=1024

PORTA_SERVER=int(PORTA_SERVER)
SERVER = (INDIRIZZO_SERVER, PORTA_SERVER)

#creazione del socket e collegamento al server
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(SERVER)
#creazione e avvio del thread che si occuperà di ricevere i messaggi
thread_ric = Thread(target=ricevi_messaggi)
thread_ric.start()
tkt.mainloop()