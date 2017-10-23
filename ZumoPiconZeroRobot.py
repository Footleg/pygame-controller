#!/usr/bin/env python3
import pygame, sys, time, math
import blinkt as blkt
import random
from PygameController import RobotController

sys.path.append('/home/pi/piconzero/')

import piconzero3 as pz

#Global variables
message = ""
    
def initStatus(status):
    """Callback function which displays status during initialisation"""
    if status == 0 :
        print("Supported controller connected")
        blkt.set_all(0,0,255)
    elif status < 0 :
        print("No supported controller detected")
        #Show red LEDs for 5 seconds before program exits and turns them all off
        blkt.set_all(255,0,0)
        blkt.show()
        time.sleep(5)
    else:
        print("Waiting for controller {}".format(status) )
        if status < 9 :
            blkt.set_pixel(status-1,255,128,0)
        elif status < 17 :
            blkt.set_pixel(status-9,255,50,0)

    blkt.show()


def leftStickChangeHandlerV2(valLR, valUD):
    """Handler function for left analogue stick"""
    mode = "Drive: "
    
    fwdpower = -valUD
    turnpower = abs(valLR)
    
    if (fwdpower == 0) and (turnpower == 0):
        mode = "Stop: "
        speedR = 0
        speedL = 0
    elif abs(fwdpower) < 0.2 :
        #Spin only, apply at max half power
        speedR = int( valLR * 64 )
        speedL = -speedR
        mode = "Spin: "
    else:    
        #Start by applying forward/reverse power to both tracks equally
        speedL = int( fwdpower * 128 )
        speedR = speedL
        
        if turnpower > 0.0 :
            #Reduce speed of one track compared to powered speed of other
            speedReduction = int( fwdpower * turnpower * 128 )
                
            #Remove turn power from one track only
            if valLR < 0.0 :
                speedR -= speedReduction
            else:
                speedL -= speedReduction

    global message
    message = mode + " Speed L: {}, Speed R: {}".format( speedL, speedR ) 

    pz.setMotor(0, speedL)
    pz.setMotor(1, speedR)


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
    ##
    
    #Run in try..finally structure so that program exits gracefully on hitting any
    #errors in the callback functions
    try:
        cnt = RobotController("Zumo Robot with Blinkt", initStatus,
                              leftStickChanged = leftStickChangeHandlerV2 )
        
        if cnt.initialised :
            keepRunning = True
            blkt.set_all(0,255,0)
            blkt.show()
        else:
            keepRunning = False
            
        # -------- Main Program Loop -----------
        while keepRunning == True :
            cnt.message = message
            
            # Trigger stick events and check for quit
            keepRunning = cnt.controllerStatus()
    
    finally:
        #Clean up and turn off Blinkt LEDs
        pz.stop()
        pz.cleanup()
        pygame.quit()
        blkt.clear()
        blkt.show()


if __name__ == '__main__':
    main()
