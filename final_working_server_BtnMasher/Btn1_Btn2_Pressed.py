#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 16:42:10 2020

@author: ubuntu
"""

import RPi.GPIO as GPIO
import time

PushBtn1 = 31
PushBtn2 = 19

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PushBtn1, GPIO.IN, pull_up_down = GPIO.PUD_UP) ## activation intern Resistance
GPIO.setup(PushBtn2, GPIO.IN, pull_up_down = GPIO.PUD_UP) 


try:
    while True:
        PushBtnState1 = GPIO.input(PushBtn1)
        PushBtnState2 = GPIO.input(PushBtn2)
        if PushBtnState1 == 1 :
            print('PushBtn1 is pushed')
            time.sleep(0.1)
        if PushBtnState2 == 1 :
            print('PushBtn2 is pushed')
            time.sleep(0.1)
        else:
            pass
except KeyboardInterrupt :
    GPIO.cleanup()    
    print('GPIO ports are cleant')