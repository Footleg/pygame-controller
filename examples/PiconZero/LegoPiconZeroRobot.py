#!/usr/bin/env python3

import sys
sys.path.append('./../../')
sys.path.append('/home/pi/4tronix/piconzero/')

import pygame, random, time, math
from PygameController import RobotController
import piconzero3 as pz

#Initialise lobal variables
steering = 90
speed = 0
minMovingSpeed = 30

# Define which output the servo is connected to
servo_no = 0

#Server min and max positions either side of centre (90 degrees)
left_limit = 58
right_limit = 110

#Multiplier applied to speed so top speed is set when stick is not quite at maximum position
speedFactor = 1.1

def initStatus(status):
    """Callback function which displays status during initialisation"""
    if status == 0 :
        print("Supported controller connected")
    elif status < 0 :
        print("No supported controller detected")
    else:
        print("Waiting for controller {}".format( status ) )
        if status % 2 > 0:
            pz.setOutput (servo_no, 95)
        else:
            pz.setOutput (servo_no, 85)
            

def powerStickChangeHandler(valLR, valUD):
    """Handler function for right analogue stick"""
    global speed
    speed = int(valUD * -100)
    if speed < 0 :
        pz.forward(-speed)
    else:
        pz.reverse(speed)



def steeringStickChangeHandler(valLR, valUD):
    global steering
    steering = int(right_limit - ( (valLR + 1) * (right_limit - left_limit) / 2 ) )
    pz.setOutput (servo_no, steering)
    

def main():
    
    ## Check that required hardware is connected ##

    #Initialise the controller board
    pz.init()

    #Confirm board detected
    vsn = pz.getRevision()
    if (vsn[1] == 2):
        print("Board Type:", "Picon Zero")
    else:
        print("Board Type:", vsn[1])
    print("Firmware version:", vsn[0])

    # Define which inputs and outputs are configured
    ## servo_no = 0
    
    # Set output modes of any Picon Zero outputs
    pz.setOutputConfig(servo_no, 2)
    
    #Run in try..finally structure so that program exits gracefully on hitting any
    #errors in the callback functions
    try:
        cnt = RobotController("Lego Picon Zero Robot", initStatus ,
                              leftStickChanged = powerStickChangeHandler,
                              rightStickChanged = steeringStickChangeHandler)
        
        if cnt.initialised :
            keepRunning = True
            #Indicate success here, we are ready to run
            pz.forward(50)
            time.sleep(0.25)
            pz.stop()
        else:
            keepRunning = False
            
        # -------- Main Program Loop -----------
        while keepRunning == True :
            cnt.message = "Servo: {}, Speed: {}" . format(steering,speed)
            
            # Trigger stick events and check for quit
            keepRunning = cnt.controllerStatus()
    
    finally:
        #Clean up and turn off Blinkt LEDs
        pz.stop()
        pz.cleanup()
        pygame.quit()


if __name__ == '__main__':
    main()
