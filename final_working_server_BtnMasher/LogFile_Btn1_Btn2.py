#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 13:27:02 2020

@author: ubuntu
"""

import csv
import time
from datetime import datetime
import RPi.GPIO as GPIO

t_begin = datetime.now().time() ## when the program starts

######

f=open('code/final_working/TestLog_PushBtn1Btn2.csv','w') ## the file of this backup 
##+str(t_begin) a ajouter si on veut avoir un nouveau fichier a chaque fois
#We can just do one database by deleting the datetime

######

writer = csv.writer(f)
l=[]

####### Define the port we are using

PushBtn1 = 31
PushBtn2 = 19

######
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PushBtn1, GPIO.IN, pull_up_down = GPIO.PUD_UP) ## activation resistance interne
GPIO.setup(PushBtn2, GPIO.IN, pull_up_down = GPIO.PUD_UP) 


Number_Test = 0 ## How many time do we pressed the button
Btn1_PressState=0
Btn1_UnpressedState=1 ## Is the button is just unpressed or was it already unpressed

Btn2_PressState=0
Btn2_UnpressedState=1 ## Is the button is just unpressed or was it already unpressed

try:
    while Number_Test < 10:
        PushBtnState1 = GPIO.input(PushBtn1)
        PushBtnState2 = GPIO.input(PushBtn2)
        if PushBtnState1 == 1  : ## If we press Btn1
            if Btn1_PressState == 0:
                print('PushBtn1 is pushed')
                t_Btn1_Pressed = datetime.now().time() 
                Btn1_PressState=1 ## Now the button1 is known as being pressed
        if PushBtnState2 == 1  : ## If we press Btn2
            if Btn2_PressState == 0:
                print('PushBtn2 is pushed')
                t_Btn2_Pressed = datetime.now().time() 
                Btn2_PressState=1 ## Now the button2 is known as being pressed
        else : ## If we dont press any Btn
            if Btn1_PressState== Btn1_UnpressedState: ## Dont want to take the initial state
                print('PushBtn1 is UNPUSHED')
                l.append([t_Btn1_Pressed,""])
                writer.writerow(l[-1])
                Number_Test+=1
                Btn1_PressState=0 # We know Btn1 is unpressed
                time.sleep(0.5)
            if Btn2_PressState== Btn2_UnpressedState: ## Dont want to take the initial state
                print('PushBtn2 is UNPUSHED')
                l.append(["",t_Btn2_Pressed])
                writer.writerow(l[-1])
                Number_Test+=1
                Btn2_PressState=0
                time.sleep(0.5)
    GPIO.cleanup()    
    print('GPIO ports are cleant')
except KeyboardInterrupt:
    GPIO.cleanup()    
    print('GPIO ports are cleant')