#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 14:33:06 2020

@author: mathieu
"""

## Definition of Client Socket with 3 parallele thread
host = '192.168.0.123'
port = 50000
import socket, sys, threading
import csv
import time


class ThreadReception(threading.Thread):
    """object thread dealing with the receiving of message"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. connection socket
        self.Btn_recv = []
        self.head = []
        self.data = []
        
    def run(self):
        i=0
        while 1:
            message_recu = self.connexion.recv(1024)
            try:
                message_recu_split = self.split_msg_recu(message_recu)
                if message_recu_split[0] == self.head[0] : ## choose where we write in the csv file
                    print(self.head[0] + " is pressed")
                    self.data.append([message_recu_split[1]," "])
                if message_recu_split[0] == self.head[1] :
                    print(self.head[1] + " is pressed")
                    self.data.append([" ",message_recu_split[1]])
                th_Ecriture.ligne_ajout_csv = self.data[-1]
            except :
                self.Btn_recv = self.split_msg_recu(message_recu)
                if i ==0:
                    self.head = self.Btn_recv
                    i +=1 ## define head just one time (did not understand why I did go in that except loop more than once)
            time.sleep(1)
            if message_recu =='' or message_recu.upper() == "FIN":
                #print('closing of the csv file')
                break # end of the ThreadReception
        th_E._Thread__stop() # we force ThreadEmission to stop
        ## Add : force the ThreadEcritureCsv to stop
        print "Client stopped. Connexion interrupted."
        self.connexion.close()
        
    def split_msg_recu(self, message_recv):
        return message_recv.split(";")
    
class ThreadEcritureCsv(threading.Thread):
    """object thread dealing with the writing of csv file"""
    def __init__(self, ligne_ajout_csv,nom_fichier):
        threading.Thread.__init__(self)
        self.ligne_ajout_csv = ligne_ajout_csv
        self.nom_fichier= nom_fichier 
        self.liste_ligne_ajout = ['']
        
        
    def run(self):
        i = 0
        while 1:
            try:
                fichier= open(self.nom_fichier,'aw')
            except:
                pass
            if self.ligne_ajout_csv != self.liste_ligne_ajout[-1]:
                writer = csv.writer(fichier)
                writer.writerow(self.ligne_ajout_csv) 
                self.liste_ligne_ajout.append(self.ligne_ajout_csv)
            i+=1
                
class ThreadEmission(threading.Thread):
    """object thread dealing with the emitting of message"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. connection socket
    def run(self):
        while 1:
            message_emis = raw_input()
            self.connexion.send(message_emis)

# Programme principal - Établissement de la connexion :
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connexion.connect((host, port))
except socket.error:
    print "Conection has failed."
    sys.exit()    
print "Connection established with the servor."
           

th_E = ThreadEmission(connexion)
th_R = ThreadReception(connexion)

th_E.start()
th_R.start()
#print('ajout de la fonction split')
time.sleep(0.5) # this solution do not work
th_Ecriture = ThreadEcritureCsv(th_R.Btn_recv,'Test_Rpi.csv') ## We create this thread after receiving the message from the number of Btn there is gonna be with their name
th_Ecriture.start()