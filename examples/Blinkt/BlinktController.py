#!/usr/bin/env python3

import sys
sys.path.append('./../../')

import pygame
from time import sleep
import blinkt as blkt
import random
from PygameController import RobotController


def randomColour(pixelIndex):
    """Sets the given pixel to a random RGB colour"""
    colR = random.randint(1, 255)
    colG = random.randint(1, 255)
    colB = random.randint(1, 255)
    blkt.set_pixel(pixelIndex,colR,colG,colB)


def colourBar(controllerValue,colR,colG,colB,reverse):
    """ Displays a bar of the given RGB colour on the Blinkt
        based on an analogue value from the controller in the
        range -1 to +1, where -1 means no pixels are lit and
        +1 means all 8 pixels are lit. The bar starts from the
        left end if 'reverse' is False, or the right end if
        'reverse' is True """
    blkt.clear()
    for i in range( 0, int( (controllerValue+1.001)*4 ) ):
        if reverse:
            idx = 7 - i
        else:
            idx = i
        blkt.set_pixel(idx,colR,colG,colB)
    blkt.show()

    
def initStatus(status):
    """Callback function which displays status during initialisation"""
    if status == 0 :
        print("Supported controller connected")
        blkt.set_all(0,0,255)
    elif status < 0 :
        print("No supported controller detected")
        for i in range(1,7):
            blkt.set_all(255,0,0)
            blkt.show()
            sleep(0.25)
            blkt.clear()
            blkt.show()
            sleep(0.25)
    else:
        print("Waiting for controller {}".format(status) )
        if status < 9 :
            blkt.set_pixel(status-1,96,0,96)
        elif status < 17 :
            blkt.set_pixel(status-9,96,96,0)
        elif status < 25 :
            blkt.set_pixel(status-17,192,40,0)
        elif status < 33 :
            blkt.set_pixel(status-25,164,2,2)

    blkt.show()


def leftTrigChangeHandler(val):
    """Handler function for left analogue trigger"""
    colourBar(val,0,196,196,False)


def rightTrigChangeHandler(val):
    """Handler function for right analogue trigger"""
    colourBar(val,255,64,64,True)


def leftStickChangeHandler(valLR, valUD):
    """Handler function for left analogue stick"""
    colR = int( (valUD + 1) * 127 )
    colG = 255 - colR
    colourBar(valLR,colR,colG,0,False)


def rightStickChangeHandler(valLR, valUD):
    """Handler function for right analogue stick"""
    colG = int( (valUD + 1) * 127 )
    colB = 255 - colG
    colourBar(-valLR,0,colG,colB,True)


def leftStickPressHandler(val):
    """Handler function for left stick press"""
    if val == 1 :
        blkt.set_all(0,28,128)
    else:
        blkt.clear()
    blkt.show()


def rightStickPressHandler(val):
    """Handler function for right stick press"""
    if val == 1 :
        blkt.set_all(255,0,0)
    else:
        blkt.clear()
    blkt.show()


def selectBtnHandler(val):
    """Handler function for Select button"""
    if val == 1 :
        blkt.set_all(180,180,0)
    else:
        blkt.clear()
    blkt.show()


def startBtnHandler(val):
    """Handler function for Start button"""
    if val == 1 :
        blkt.set_all(0,140,28)
    else:
        blkt.clear()
    blkt.show()


def leftFrontBtn1Handler(val):
    """Handler function for Front Left button 1"""
    if val == 1 :
        blkt.set_all(0,128,128)
    else:
        blkt.clear()
    blkt.show()


def rightFrontBtn1Handler(val):
    """Handler function for Front Right button 1"""
    if val == 1 :
        blkt.set_all(128,0,128)
    else:
        blkt.clear()
    blkt.show()


def leftFrontBtn2Handler(val):
    """Handler function for Front Left button 2"""
    if val == 1 :
        blkt.set_all(64,64,0)
    else:
        blkt.clear()
    blkt.show()


def rightFrontBtn2Handler(val):
    """Handler function for Front Right button 2"""
    if val == 1 :
        blkt.set_all(24,200,0)
    else:
        blkt.clear()
    blkt.show()


def hatBtnHandler(valUD,valLR):
    if valUD == 1 :
        randomColour(0)
    elif valUD == -1 :
        randomColour(1)
    elif valLR == -1 :
        randomColour(2)
    elif valLR == 1 :
        randomColour(3)
    blkt.show()

def triangleBtnHandler(val):
    if val == 1 :
        randomColour(4)
    blkt.show()


def squareBtnHandler(val):
    if val == 1 :
        randomColour(5)
    blkt.show()


def circleBtnHandler(val):
    if val == 1 :
        randomColour(6)
    blkt.show()


def crossXBtnHandler(val):
    if val == 1 :
        randomColour(7)
    blkt.show()


def main():
    #Run in try..finally structure so that program exits gracefully on hitting any
    #errors in the callback functions
    try:
        cnt = RobotController("Game Controller Blinkt Tester", initStatus,
                              leftTriggerChanged = leftTrigChangeHandler,
                              rightTriggerChanged = rightTrigChangeHandler,
                              leftStickChanged = leftStickChangeHandler,
                              rightStickChanged = rightStickChangeHandler, 
                              leftStickPressChanged = leftStickPressHandler,
                              rightStickPressChanged = rightStickPressHandler,
                              leftBtn1Changed = leftFrontBtn1Handler,
                              rightBtn1Changed = rightFrontBtn1Handler,
                              leftBtn2Changed = leftFrontBtn2Handler,
                              rightBtn2Changed = rightFrontBtn2Handler,
                              selectBtnChanged = selectBtnHandler,
                              startBtnChanged = startBtnHandler,
                              hatChanged = hatBtnHandler,
                              triangleBtnChanged = triangleBtnHandler,
                              squareBtnChanged = squareBtnHandler,
                              circleBtnChanged = circleBtnHandler,
                              crossXBtnChanged = crossXBtnHandler
                              )

        if cnt.initialised :
            keepRunning = True
            blkt.set_all(0,255,0)
            blkt.show()
        else:
            keepRunning = False
            
        # -------- Main Program Loop -----------
        while keepRunning == True :
            # Trigger stick events and check for quit
            keepRunning = cnt.controllerStatus()
    
    finally:
        #Clean up and turn off Blinkt LEDs
        pygame.quit()
        if cnt.initialised :
            blkt.clear()
            blkt.show()

if __name__ == '__main__':
    main()
    