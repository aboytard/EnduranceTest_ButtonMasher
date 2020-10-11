# EnduranceTest_ButtonMasher
Here is only the socket server between Rpi and Laptop + detection buttom pressed


BUTTON NOT CONNECTED TO THE URe5

## Step 0: Test if the button are well connected

--> /!\ Issue: In the tutorial, we should have a PushBtnState 0 value when the button is pressed. However, in this case, it is working with the PushBtnState == 1:
so this method has to be run firstly --> Btn1_Btn2_Pressed.py

## Step1: Make sure that the socket is connecting to the right IP address and good port

--> /!\ Issue: Normally, I should have set a static IP adress but I did not know why the Rpi was not working with the dhcpcd.conf file at first. I am also changing places the Rpi and the laptop to work so changing the network.

## Step2: Make sure you have connected the Buttons to the right GPIO.

--> /!\ Issue with step 2: The code was written to use 2 buttons at the time (to object of the class ThreadSendBtnMsg are created) and I have to figure out how to enable the code to write in the right case if there are more than 2 buttons (ThreadEcritureCsv)


## Step3: Close the connection between the client and the server
Raw input : 'END'
--> /!\ Issue: I do not manage to close the socket server with the same scheme

Improvement that can be done: 
- Use new title for every new test running like (LogFile_ + str(datetime) ) + create a repo for every log file to be logged into (with a global path)
- Solve Step 2
- Add the delay between Raising and Failing Edge
--> /!\ Issue: The Gpio standard function to detect every change is detected way more than just raising and failing. Therefore there are two many factors that change the post processing to calculate the delay. I got a function that were right but succeed 1 on 2 times.. Moreover, I cannot globalize the value I had with the succeeded try, because I am the one pressing the button (I am not pressing it the same way every time).
- Write Every Thread in a different script so it can be reused afterwards in different program
