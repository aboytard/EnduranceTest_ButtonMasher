#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 16:18:18 2020

@author: mathieu
"""

# Définition d'un serveur réseau gérant un système de CHAT simplifié.
# Utilise les threads pour gérer les connexions clientes en parallèle.
HOST = '192.168.0.123'
PORT = 50000
import socket, sys, threading
import time
from datetime import datetime
import RPi.GPIO as GPIO
import csv

class ThreadSendBtnMsg(threading.Thread):
    '''dérivation d'un objet thread pour gérer l envoi de message a l appuie d un bouton'''
    def __init__(self, conn,PushBtn_Port):
        threading.Thread.__init__(self)
        self.connexion = conn
        self.PushBtn_Port = PushBtn_Port
        self.name = "Btn_%s" %PushBtn_Port
        self.Number_Test = 0
        self.Btn_indicatorPush = 0 
        self.Btn_indicatorUnpush = 1 ## if Btn1_indicatorPush == Btn1_indicatorUnpush
        self.list_datetime = []
        self.head = []
        
        
    def run(self):
        while self.Number_Test < 100:
            msgServer = "salut coco"
            PushBtnState = GPIO.input(self.PushBtn_Port)
            if PushBtnState == 1  :
                print(self.name + ' is pushed')
                t_Btn_Pressed = self.name + ";" +str(datetime.now().time()) ## Add a separator to make things easier for the future
                self.Btn_indicatorPush = 1
            else:
                if self.Btn_indicatorPush == self.Btn_indicatorUnpush: ## Dont want to take the initial state
                    print(self.name + ' is UNPUSHED')
                    self.list_datetime.append([t_Btn_Pressed])
                    self.Number_Test+=1
                    msgServer = str(t_Btn_Pressed) 
                    try:
                        th_Writer.line_add_csv = th_Writer.split_msg_towrite(t_Btn_Pressed,head)
                        print(th_Writer.line_add_csv)
                    except:
                        print("probleme sur la fonction split")
                    self.connexion.send(msgServer)
                    self.Btn_indicatorPush=0          
            

            

class ThreadClient(threading.Thread):
    '''dérivation d'un objet thread pour gérer la connexion avec un client'''
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
        
    def run(self):
        # Dialog with the client :
        nom = self.getName()        # get the name of each thread client connected
        while 1:
            msgClient = self.connexion.recv(1024)
            if msgClient.upper() == "END" or msgClient =="":
                break
            message = "%s> %s" % (nom, msgClient)
            print message
            # Faire suivre le message à tous les autres clients :
            for cle in conn_client:
                if cle != nom:      # ne pas le renvoyer à l'émetteur
                    conn_client[cle].send(message)
                    
        # Fermeture de la connexion :
        self.connexion.close()      # cut connexion from the server with client
        del conn_client[nom]        # supprimer son entrée dans le dictionnaire
        print "Client %s disconnected." % nom
        # Le thread se termine ici    

        
        
class ThreadEcritureCsv(threading.Thread):
   '''object thread dealing with the writing of the log file in the Rpi'''
   def __init__(self, line_add_csv, name_file):
       threading.Thread.__init__(self)
       self.line_add_csv = line_add_csv
       self.name_file = name_file
       self.list_line_add = [line_add_csv]
       
   def run(self):
       i=0
       while 1:  
           
           try:
               file = open(self.name_file,'aw') # Open the file
           except :
               pass
           writer = csv.writer(file) ## Have to put there to not have error
           if self.line_add_csv != self.list_line_add[-1]:
               writer.writerow(self.line_add_csv)
               self.list_line_add.append(self.line_add_csv) ## we add in only after writing it
           time.sleep(1)
           i += 1
           
   def split_msg_towrite(self,msgServer,column_towrite):
       msg_writen = msgServer.split(";")
       if msg_writen[0] == column_towrite[0]:
           return [msg_writen[1],'']
       if msg_writen[0] == column_towrite[1]:
           return ['',msg_writen[1]]
       else:
           print("No Message to write??")
           pass       

# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print "The link with the chosen address socket failed."
    sys.exit()
print "Servor ready, waiting for answer.."
mySocket.listen(5)

# Attente et prise en charge des connexions demandées par les clients :
conn_client = {}                # dictionnaire des connexions clients
stop_thread = False

PushBtn1 = 31
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PushBtn1, GPIO.IN, pull_up_down = GPIO.PUD_UP) ## activati

PushBtn2 = 19
GPIO.setup(PushBtn2, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while 1:    
    connexion, adresse = mySocket.accept()
    # Créer un nouvel objet thread pour gérer la connexion :
    th_Client = ThreadClient(connexion)
    th_Btn1 = ThreadSendBtnMsg(connexion,PushBtn1)
    th_Btn2 = ThreadSendBtnMsg(connexion,PushBtn2)
    th_Client.start()
    th_Btn1.start()
    th_Btn2.start()
    head = [th_Btn1.name,th_Btn2.name] #### DO BETTER
    th_Writer = ThreadEcritureCsv(head,'Test_Rpi_FINAL.csv') ## DO BETTER INIT = DO WITH POSSIBILITY OF ADD n BTN
    print ([th_Btn1.name,th_Btn2.name])
    th_Writer.start()
    # Mémorize connection in dictionnary 
    it = th_Client.getName()        # id of thread
    conn_client[it] = connexion
    print "Client %s connecté, adresse IP %s, port %s." %\
           (it, adresse[0], adresse[1])
    # Dialogue avec le client :
#    connexion.send("You are connected. Send your message.")
    connexion.send(th_Btn1.name + ";" + th_Btn2.name) ## in order to initialiwe well the client list of datetime
    ## FIND A WAY TO AUTOMISE THIS (every time a button is add, a new column appears)
    


