#!/usr/bin/env python3

"""
    Example driving twin motors for skid steering using the Rocky Rover HAT.
"""

#Add folder containing PygameController module to the system path
#(only needed if PygameController is in a different folder to your program)
import sys
sys.path.append('./../../')

#Import the modules your code uses. These have to include pygame and the
#PygameController module
import pygame
from PygameController import RobotController
import RockyRoverHAT as rh

#Initialise global variables
power = 0
turn = 0
message = ""

#The controller program needs an initialisation status callback function to send status codes
#to while the program looks for a supported game controller. This function will get called
#with status values counting up from 1 to 32 while it waits for a wireless controller to be
#paired using bluetooth, or for a usb dongle to be inserted or usb wired controller.
#If no supported controller is detected it will eventually be called with the status value -1
#Once a supported controller is detected it will return a status code of zero.
def initStatus(status):
    """ Function which displays status during initialisation """
    if status == 0 :
        print("Supported controller connected")
    elif status < 0 :
        print("No supported controller detected")
    else:
        print("Waiting for controller {}".format(status) )


#--- Start of example call back functions for different type of controls on game controllers ---
def analogueTriggerChangeHandler(val):
    """ Handler function for an analogue trigger """
    print("Analogue Trigger Value Changed: {}".format(val) )


def leftStickChangeHandler(valLR, valUD):
    """Handler function for left analogue stick"""
    global power
    power = valUD


def rightStickChangeHandler(valLR, valUD):
    """Handler function for right analogue stick"""
    global turn
    turn = valLR


def hatHandler(valLR, valUD):
    """ Handler function for an joystick hat """
    print("Digital Hat Changed: L/R:{} U/D:{}".format(valLR,valUD) )


def btnHandler(val):
    """ Handler function for a button """
    print("Button State Changed. Value={}".format(val) )


def triangleBtnHandler(val):
    """ Handler function for the triangle button """
    if val == 1 :
        print("Triangle button pressed")
    else:
        print("Triangle button released")

#--------------------- End of example change handler call back functions --------------------

def motorSpeed(ls,rs):
    """ Sets percentage power for left and right motors based on left and right stick positions
        of game controller. If power (left) stick is at zero position then right stick will
        control spot turn with variable power. Otherwise steering will reduce power to the inside
        motor from the level of the power stick up to maximum of the reversed speed of the motor
        on the outside of the turn.
    """
    global message
    lm = 0
    rm = 0

    if ls == 0 :
        #No power stick, so use right stick for spot turning
        lm = rs * 100
        rm = -lm
    elif rs == 0 :
        #No turning, so use left stick for forward/backwards power
        lm = -ls * 100
        rm = lm
    elif rs < 0 :
        #Turning left while moving
        rm = -ls * 100
        lm = rm + rs * 2 * rm
    else :
        #Turn right while moving
        lm = -ls * 100
        rm = lm - rs * 2 * lm

    message = "lm = {}, rm = {}".format( int(lm), int(rm) )

    #set the power for each motor
    rh.setMotorsPower(lm,rm)


#This is the main function of the program.
def main():
    """ Main program code. This function creates an instance of the robot controller class
        and passes in all the call back functions which will be called when the state of the
        associated buttons, joysticks and triggers on the game controller changes.
    """
    #Check any hardward you are using is present and initialise it here
    print("Initialising hardware")

    #Use a try..finally structure so that the program exits gracefully on hitting any
    #errors in the callback functions and cleans up any hardware you are using.
    try:
        cnt = RobotController("Game Controller Template Program", initStatus,
                              leftTriggerChanged = analogueTriggerChangeHandler,
                              leftStickChanged = leftStickChangeHandler,
                              rightStickChanged = rightStickChangeHandler,
                              hatChanged = hatHandler,
                              startBtnChanged = btnHandler,
                              triangleBtnChanged = triangleBtnHandler
                              )

        #Check if the controller class initialised successfully
        if cnt.initialised :
            keepRunning = True
            #You can put any code here you want to use to indicate that a supported game
            #controller is connected and the program is ready. (e.g. Flash some LEDs green)
        else:
            keepRunning = False
            #You can put any code here you want to use to indicate that no supported game
            #controller was detected (the program will exit afterwards). e.g. Flash some LEDs red

        # -------- Main Program Loop -----------
        while keepRunning == True :
            #You have to call the controllerStatus function in a loop, as this is what
            #triggers any callback functions for controller state changes. It also checks for
            #the quit event (occurs when the pygame window is closed by a user), and returns
            #False if this happens. So the return value is used to exit the loop on quit.
            keepRunning = cnt.controllerStatus()

            #Update motor speeds
            motorSpeed(power, turn)
            cnt.message = message



    finally:
        #Clean up pygame and any hardware you may be using
        #(e.g. Turn off LEDs and power down motors)
        pygame.quit()
        if cnt.initialised :
            #Put any clean up code for your program here
            print("Cleaning up")
            rh.allOff()


if __name__ == '__main__':
    main()