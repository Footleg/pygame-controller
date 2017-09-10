#!/usr/bin/env python3

#Import lines for dev build of pygame on ubuntu (remove these for raspberry pi)
import sys
sys.path.append('/usr/local/lib/python3.5/dist-packages/pygame-1.9.4.dev0-py3.5-linux-i686.egg')

import pygame


class TextPrint:
    """Simple class to help display text information in the application window"""
    BLACK    = (   0,   0,   0)
    WHITE    = ( 255, 255, 255)
    
    def __init__(self, screen):
        self.screen = screen
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, textString):
        textBitmap = self.font.render(textString, True, self.BLACK)
        self.screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        self.screen.fill(self.WHITE)
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
    

class RobotController:
    """Provides a Pygame based application to detect controller input
    and interface the controller to your own code.

    """
    
    #Data for supported controllers
    SUPPORTED_JOYSTICKS = ("PLAYSTATION(R)3 Controller","Sony PLAYSTATION(R)3 Controller",
                           "Performance Designed Products Rock Candy Wireless Gamepad for PS3")
    DETECTED_JOYSTICK_IDX = -1
    
    #Define specifications of each supported controller
    AXES = (27,4)
    BTNS = (19,13)
    HATS = (0,1)
    
    #Define indices for each control for the different supported controllers
    leftTriggerIdx = (12,-1)
    rightTriggerIdx = (13,-1)
    leftStickLRIdx = (0,0)
    leftStickUDIdx = (1,1)
    rightStickLRIdx = (2,2)
    rightStickUDIdx = (3,3)
    leftBtn1Idx = (10,4)
    rightBtn1Idx = (11,5)
    leftBtn2Idx = (8,6)
    rightBtn2Idx = (9,7)
    hatLeftIdx = (7,-1)
    hatRightIdx = (5,-1)
    hatUpIdx = (4,-1)
    hatDownIdx = (6,-1)
    hatIdx = (-1,0)
    leftStickPressIdx = (1,10)
    rightStickPressIdx = (2,11)
    selectBtnIdx = (0,8)
    startBtnIdx = (3,9)
    triangleBtnIdx = (12,3)
    squareBtnIdx = (15,0)
    circleBtnIdx = (13,2)
    crossXBtnIdx = (14,1)

    initialised = False
    
    #Message text to be displayed in window which can be set from outside the class
    message = ""
    
    # Flags to indicate when triggers have been used. The triggers report 0.0 until
    # first pressed, but should be sending -1.0 in their rest positions. These flags
    # are used to prevent the program giving a false reading before the triggers have
    # had their first use.
    leftTriggerActivated = False
    rightTriggerActivated = False

    #Initialise controller trigger and button states to their rest position values
    leftTriggerPos = -1.0
    rightTriggerPos = -1.0
    leftStickLR = 0.0
    leftStickUD = 0.0
    rightStickLR = 0.0
    rightStickUD = 0.0
    leftBtn1State = 0
    rightBtn1State = 0
    leftBtn2State = 0
    rightBtn2State = 0
    hatLRState = 0
    hatUDState = 0
    leftStickPressedState = 0
    rightStickPressedState = 0
    selectBtnState = 0
    startBtnState = 0
    triangleBtnState = 0
    squareBtnState = 0
    circleBtnState = 0
    crossXBtnState = 0
    
    def __init__(self, title, initStatus, leftTriggerChanged = None, rightTriggerChanged = None,
                 leftStickChanged = None, rightStickChanged = None,
                 leftBtn1Changed = None, rightBtn1Changed = None,
                 leftBtn2Changed = None, rightBtn2Changed = None,
                 hatChanged = None,
                 leftStickPressChanged = None, rightStickPressChanged = None,
                 selectBtnChanged = None, startBtnChanged = None, triangleBtnChanged = None,
                 squareBtnChanged = None, circleBtnChanged = None, crossXBtnChanged = None ):
        """ Robot controller initialisation function. Enables callback functions to be passed
            in for the following events:
            
            Args:
                title: The text to be displayed on the application window title bar
                
                initStatus: A callback function which will be passed integer status values
                    during initialisation of the application. The function given as this argument
                    will be called while the application is detecting a supported game controller.
                    A status code of 0 indicates a controller was successfully detected.
                    Status codes in the range 1 - 16 indicate attempts to detect a controller. While
                    these values are being returned, the application is waiting for a controller to
                    be connected (via cable or bluetooth). The status value indicates how many
                    attempts have been made. After 16 attempts if no supported controller has been
                    detected then the application will return the status code -1, and then exit.
                
                leftTriggerChanged: A callback function which will be passed the position value of
                    the left analogue trigger. This function will only be called when the trigger
                    value changes, so your application code will only be called when something needs
                    to be updated.
                
                rightTriggerChanged: A callback function for the right trigger (see leftTriggerChanged)

                leftStickChanged: A callback function which will be passed the position value of
                    the left analogue stick as pair of floats consisting the left/right position and up/down
                    positions of the stick. This function will only be called when the stick
                    position changes, so your application code will only be called when something needs
                    to be updated.
                
                rightStickChanged: A callback function for the right stick (see leftStickChanged)
                
                leftBtn1Changed: A callback function which is called when the state of the left front button 1
                    on the controller changes. It will be passed an integer value indicating whether the button
                    is pressed (1) or released (0)
                
                rightBtn1Changed: A callback function for the right front button 1 (see leftBtn1Changed)
                
                leftBtn2Changed: A callback function for the left front button 2 (see leftBtn1Changed)
                
                rightBtn2Changed: A callback function for the right front button 2 (see leftBtn1Changed)
                
                hatChanged: A callback function which will be passed the states of the buttons on
                    the 4-way hat as a pair of integers representing the Up/Down and Left/Right states of the
                    hat buttons. The Up/Down state = 1 for up, 0 for centre and -1 for down. The Left/Right
                    state = -1 for left, 0 for centre and 1 for right. This function will only be called when the 
                    hat state changes, so your application code will only be called when something needs
                    to be updated.
                
                leftStickPressChanged: A callback function for the left stick pressed state (see leftBtn1Changed)
                
                rightStickPressChanged: A callback function for the right stick pressed state (see leftBtn1Changed)
                
                selectBtnChanged: A callback function for the Select button (see leftBtn1Changed)
                
                startBtnChanged: A callback function for the Start button (see leftBtn1Changed)
                
                triangleBtnChanged: A callback function for the triangle symbol button (see leftBtn1Changed)
                
                squareBtnChanged: A callback function for the square symbol button (see leftBtn1Changed)
                
                circleBtnChanged: A callback function for the circle symbol button (see leftBtn1Changed)
                
                crossXBtnChanged: A callback function for the X symbol button (see leftBtn1Changed)
                
        """
        #Storereferences to callback functions
        self.initStatus = initStatus
        self.leftTriggerChanged = leftTriggerChanged
        self.rightTriggerChanged = rightTriggerChanged
        self.leftStickChanged = leftStickChanged
        self.rightStickChanged = rightStickChanged
        self.leftBtn1Changed = leftBtn1Changed
        self.rightBtn1Changed = rightBtn1Changed
        self.leftBtn2Changed = leftBtn2Changed
        self.rightBtn2Changed = rightBtn2Changed
        self.hatChanged = hatChanged
        self.leftStickPressChanged = leftStickPressChanged
        self.rightStickPressChanged = rightStickPressChanged
        self.selectBtnChanged = selectBtnChanged
        self.startBtnChanged = startBtnChanged
        self.triangleBtnChanged = triangleBtnChanged
        self.squareBtnChanged = squareBtnChanged
        self.circleBtnChanged = circleBtnChanged
        self.crossXBtnChanged = crossXBtnChanged
        
        #Look for supported game controller
        controllerFound = False
        lastCount = 0
        for retries in range(1, 17):
            #Initialise pygame
            pygame.init()

            # Initialize the joysticks
            pygame.joystick.init()
            
            # Get count of joysticks
            joystick_count = pygame.joystick.get_count()
            
            #Examine joysticks if number changed
            if lastCount != joystick_count :
                lastCount = joystick_count

                for i in range(joystick_count):
                    joystick = pygame.joystick.Joystick(i)
                    joystick.init()

                    # Get the name from the OS for the controller/joystick
                    name = joystick.get_name()
                    
                    if name in self.SUPPORTED_JOYSTICKS :
                        print("Joystick {} detected as ".format(i) + name )
                        
                        #Determine which joystick type was detected
                        for i in range(0, len(self.SUPPORTED_JOYSTICKS)-1) :
                            if name == self.SUPPORTED_JOYSTICKS[i] :
                                if i < 2 :
                                    #Genuine Sony PS3 Dualshock 6 axis controller
                                    self.DETECTED_JOYSTICK_IDX = 0
                                else :
                                    #Rock Candy PS3 controller
                                    self.DETECTED_JOYSTICK_IDX = 1
                                break
                                    
                        #Check the controller matches the expected specifications
                        axes = joystick.get_numaxes()
                        if axes == self.AXES[self.DETECTED_JOYSTICK_IDX] :
                            hats = joystick.get_numhats()
                            if hats == self.HATS[self.DETECTED_JOYSTICK_IDX] :
                                btns = joystick.get_numbuttons()
                                if btns == self.BTNS[self.DETECTED_JOYSTICK_IDX] :
                                    #Set up this controller
                                    self.controller = joystick
                                    controllerFound = True
                                    
                                    #Send status success to callback function
                                    self.initStatus(0)
                                    break
                                else:
                                    print("Joystick has {} buttons. Expected {}.".format( btns,self.BTNS[self.DETECTED_JOYSTICK_IDX] ) )
                            else:
                                print("Joystick has {} hats. Expected {}.".format( hats,self.HATS[self.DETECTED_JOYSTICK_IDX] ) )
                        else:
                            print("Joystick has {} axes. Expected {}.".format( axes,self.AXES[self.DETECTED_JOYSTICK_IDX] ) )
                    else:
                        print("Unsupported joystick {} detected as ".format(i) + name )
                        
            #Retry if controller was not detected
            if controllerFound == False :
                #Ready to try again
                self.initStatus(retries)
                self.DETECTED_JOYSTICK_IDX = -1
                #Quit pygame as it needs restarting to detect newly paired joysticks
                pygame.quit()
            else:
                 break
        
        #Finished trying to detect game controller             
        if controllerFound == False :
            #Send status failed to callback function
            self.initStatus(-1)
        else:
            #Complete class set up
            
            # Set the width and height of the screen [width,height]
            size = [500, 700]
            self.screen = pygame.display.set_mode(size)

            pygame.display.set_caption(title)

            # Used to manage how fast the screen updates
            self.clock = pygame.time.Clock()

            # Create text output object 
            self.textPrint = TextPrint(self.screen)

            self.textPrint.print("Controller Detected: {}".format( self.controller.get_name() ) )
    
            # Update the screen 
            pygame.display.flip()
            
            #Set initialised flag to indicate everything is ready
            self.initialised = True
    
    
    def controllerStatus(self):
        """Checks the status of controller inputs, calling any defined callback functions.
           Displays the status of all controls on screen and returns a flag indicating whether to quit.
           
           This function should be called in a loop from your application as often as your code can. It
           will automatically regulate the frequency it is called using the pygame clock.
        """
        
        #Initialise screen display of controller status
        self.textPrint.reset()
        self.textPrint.print("Controller: {}".format( self.controller.get_name() ) )
        self.textPrint.indent()
        
        #Process analogue sticks
        if (self.leftStickLRIdx[self.DETECTED_JOYSTICK_IDX] != -1
        and self.leftStickUDIdx[self.DETECTED_JOYSTICK_IDX] != -1 ):
            #Get stick postitions
            leftStickLR = self.controller.get_axis( self.leftStickLRIdx[self.DETECTED_JOYSTICK_IDX] )
            leftStickUD = self.controller.get_axis( self.leftStickUDIdx[self.DETECTED_JOYSTICK_IDX] )
            #Display stick position on screen
            self.textPrint.print("Left Stick:" )
            self.textPrint.indent()
            self.textPrint.print("Left/Right: {}".format( leftStickLR ) )
            self.textPrint.print("Up/Down: {}".format( leftStickUD ) )
            self.textPrint.unindent()
            #Call the callback function if defined and stick position has changed since last called
            if (self.leftStickChanged is not None
            and ( self.leftStickLR != leftStickLR or self.leftStickUD != leftStickUD ) ):
                self.leftStickLR = leftStickLR
                self.leftStickUD = leftStickUD
                self.leftStickChanged( self.leftStickLR, self.leftStickUD )
                
        if (self.rightStickLRIdx[self.DETECTED_JOYSTICK_IDX] != -1
        and self.rightStickUDIdx[self.DETECTED_JOYSTICK_IDX] != -1 ):
            #Get stick postitions
            rightStickLR = self.controller.get_axis( self.rightStickLRIdx[self.DETECTED_JOYSTICK_IDX] )
            rightStickUD = self.controller.get_axis( self.rightStickUDIdx[self.DETECTED_JOYSTICK_IDX] )
            #Display stick position on screen
            self.textPrint.print("Right Stick:" )
            self.textPrint.indent()
            self.textPrint.print("Left/Right: {}".format( rightStickLR ) )
            self.textPrint.print("Up/Down: {}".format( rightStickUD ) )
            self.textPrint.unindent()
            #Call the callback function if defined and stick position has changed since last called
            if (self.rightStickChanged is not None
            and ( self.rightStickLR != rightStickLR or self.rightStickUD != rightStickUD ) ):
                self.rightStickLR = rightStickLR
                self.rightStickUD = rightStickUD
                self.rightStickChanged( self.rightStickLR, self.rightStickUD )
                
        #Process analogue triggers
        self.textPrint.print("Front Analogue Triggers:" )
        self.textPrint.indent()
        if self.leftTriggerIdx[self.DETECTED_JOYSTICK_IDX] != -1 :
            #Get trigger value
            leftTrigger = self.controller.get_axis( self.leftTriggerIdx[self.DETECTED_JOYSTICK_IDX] )
            #Analogue triggers return zero until first used, even through their rest status is -1
            #so we need to detect the first time they return a non-zero value to activate them and
            #start returning their value to the callback function.
            if self.leftTriggerActivated == False :
                if leftTrigger != 0.0 :
                    self.leftTriggerActivated = True
            #Display value on screen
            self.textPrint.print("Left Trigger: {}".format( leftTrigger ) )
            #Call the callback function if defined and trigger position has changed since last called
            if (self.leftTriggerChanged is not None
            and self.leftTriggerActivated == True
            and self.leftTriggerPos != leftTrigger ):
                self.leftTriggerPos = leftTrigger
                self.leftTriggerChanged( self.leftTriggerPos )
        else:
            self.textPrint.print("No analogue Left Trigger on this controller" )
            
        if self.rightTriggerIdx[self.DETECTED_JOYSTICK_IDX] != -1:
            #Get trigger value
            rightTrigger = self.controller.get_axis( self.rightTriggerIdx[self.DETECTED_JOYSTICK_IDX] )
            #Analogue triggers return zero until first used, even through their rest status is -1
            #so we need to detect the first time they return a non-zero value to activate them and
            #start returning their value to the callback function.
            if self.rightTriggerActivated == False :
                if rightTrigger != 0.0 :
                    self.rightTriggerActivated = True
            #Display value on screen
            self.textPrint.print("Right Trigger: {}".format( rightTrigger ) )
            #Call the callback function if defined and trigger position has changed since last called
            if (self.rightTriggerChanged is not None
            and self.rightTriggerActivated == True
            and self.rightTriggerPos != rightTrigger ):
                self.rightTriggerPos = rightTrigger
                self.rightTriggerChanged( self.rightTriggerPos )
        else:
            self.textPrint.print("No analogue Left Trigger on this controller" )

        self.textPrint.unindent()
        
        #Process Hats
        if self.hatIdx[self.DETECTED_JOYSTICK_IDX] != -1:
            hatState = self.controller.get_hat( self.hatIdx[self.DETECTED_JOYSTICK_IDX] )
            hatLR = hatState[0]
            hatUD = hatState[1]
            self.textPrint.print("4-way hat:" )
            self.textPrint.indent()
            self.textPrint.print("Left/Right: {}".format( hatLR ) )
            self.textPrint.print("Up/Down: {}".format( hatUD ) )
            self.textPrint.unindent()
        elif (self.hatUpIdx[self.DETECTED_JOYSTICK_IDX] != -1
        and   self.hatDownIdx[self.DETECTED_JOYSTICK_IDX] != -1
        and   self.hatLeftIdx[self.DETECTED_JOYSTICK_IDX] != -1
        and   self.hatRightIdx[self.DETECTED_JOYSTICK_IDX] != -1 ):
            #Process hat buttons where detected as separate buttons
            hatUpBtn = self.controller.get_button( self.hatUpIdx[self.DETECTED_JOYSTICK_IDX] )
            hatDownBtn = self.controller.get_button( self.hatDownIdx[self.DETECTED_JOYSTICK_IDX] )
            if hatUpBtn == 1 :
                hatUD = 1
            elif hatDownBtn == 1 :
                hatUD = -1
            else:
                hatUD = 0
            hatLeftBtn = self.controller.get_button( self.hatLeftIdx[self.DETECTED_JOYSTICK_IDX] )
            hatRightBtn = self.controller.get_button( self.hatRightIdx[self.DETECTED_JOYSTICK_IDX] )
            if hatLeftBtn == 1 :
                hatLR = -1
            elif hatRightBtn == 1 :
                hatLR = 1
            else:
                hatLR = 0
            self.textPrint.print("4-way hat buttons:" )
            self.textPrint.indent()
            self.textPrint.print("Left: {}".format( hatLeftBtn ) )
            self.textPrint.print("Right: {}".format( hatRightBtn ) )
            self.textPrint.print("Up: {}".format( hatUpBtn ) )
            self.textPrint.print("Down: {}".format( hatDownBtn ) )
            self.textPrint.unindent()
            self.textPrint.print("Converted to Hat values:" )
            self.textPrint.indent()
            self.textPrint.print("Left/Right: {}".format( hatLR ) )
            self.textPrint.print("Up/Down: {}".format( hatUD ) )
            self.textPrint.unindent()
                
        #Update Hat state if any button states changed
        if (self.hatChanged is not None
        and (self.hatUDState != hatUD or self.hatLRState != hatLR) ):
            self.hatUDState = hatUD
            self.hatLRState = hatLR
            self.hatChanged( self.hatUDState, self.hatLRState )
        
        #Process buttons
        self.textPrint.print("Simple buttons:" )
        self.textPrint.indent()
        self.leftStickPressedState = self.processButton(
            self.leftStickPressIdx[self.DETECTED_JOYSTICK_IDX],
            "Left Stick Pressed", self.leftStickPressedState, self.leftStickPressChanged)
        
        self.textPrint.unindent()
        
        """
        rightStickPress = self.controller.get_button( self.rightStickPressIdx[self.DETECTED_JOYSTICK_IDX] )
        self.textPrint.print("Right Stick Pressed: {}".format( rightStickPressedState ) )
        if self.leftStickPressedState != leftStickPress :
            self.leftStickPressedState = leftStickPress
            if self.leftStickPressChanged is not None :
                self.leftStickPressChanged( self.leftStickPressedState )
        if self.rightStickPressedState != rightStickPress :
            self.rightStickPressedState = rightStickPress
            if self.rightStickPressChanged is not None :
                self.rightStickPressChanged( self.rightStickPressedState )
        """
        
        leftBtn1 = self.controller.get_button( self.leftBtn1Idx[self.DETECTED_JOYSTICK_IDX] )
        rightBtn1 = self.controller.get_button( self.rightBtn1Idx[self.DETECTED_JOYSTICK_IDX] )
        leftBtn2 = self.controller.get_button( self.leftBtn2Idx[self.DETECTED_JOYSTICK_IDX] )
        rightBtn2 = self.controller.get_button( self.rightBtn2Idx[self.DETECTED_JOYSTICK_IDX] )
        selectBtn = self.controller.get_button( self.selectBtnIdx[self.DETECTED_JOYSTICK_IDX] )
        startBtn = self.controller.get_button( self.startBtnIdx[self.DETECTED_JOYSTICK_IDX] )
        triangleBtn = self.controller.get_button( self.triangleBtnIdx[self.DETECTED_JOYSTICK_IDX] )
        squareBtn = self.controller.get_button( self.squareBtnIdx[self.DETECTED_JOYSTICK_IDX] )
        circleBtn = self.controller.get_button( self.circleBtnIdx[self.DETECTED_JOYSTICK_IDX] )
        crossXBtn = self.controller.get_button( self.crossXBtnIdx[self.DETECTED_JOYSTICK_IDX] )

        
        #Update button states if changed
        if self.leftBtn1State != leftBtn1 :
            self.leftBtn1State = leftBtn1
            if self.leftBtn1Changed is not None :
                self.leftBtn1Changed( self.leftBtn1State )
        if self.rightBtn1State != rightBtn1 :
            self.rightBtn1State = rightBtn1
            if self.rightBtn1Changed is not None :
                self.rightBtn1Changed( self.rightBtn1State )
        if self.leftBtn2State != leftBtn2 :
            self.leftBtn2State = leftBtn2
            if self.leftBtn2Changed is not None :
                self.leftBtn2Changed( self.leftBtn2State )
        if self.rightBtn2State != rightBtn2 :
            self.rightBtn2State = rightBtn2
            if self.rightBtn2Changed is not None :
                self.rightBtn2Changed( self.rightBtn2State )
        if self.selectBtnState != selectBtn :
            self.selectBtnState = selectBtn
            if self.selectBtnChanged is not None :
                self.selectBtnChanged( self.selectBtnState )
        if self.startBtnState != startBtn :
            self.startBtnState = startBtn
            if self.startBtnChanged is not None :
                self.startBtnChanged( self.startBtnState )
        if self.triangleBtnState != triangleBtn :
            self.triangleBtnState = triangleBtn
            if self.triangleBtnChanged is not None :
                self.triangleBtnChanged( self.triangleBtnState )
        if self.squareBtnState != squareBtn :
            self.squareBtnState = squareBtn
            if self.squareBtnChanged is not None :
                self.squareBtnChanged( self.squareBtnState )
        if self.circleBtnState != circleBtn :
            self.circleBtnState = circleBtn
            if self.circleBtnChanged is not None :
                self.circleBtnChanged( self.circleBtnState )
        if self.crossXBtnState != crossXBtn :
            self.crossXBtnState = crossXBtn
            if self.crossXBtnChanged is not None :
                self.crossXBtnChanged( self.crossXBtnState )
        """                
        self.textPrint.print("Front Buttons No.1:" )
        self.textPrint.indent()
        self.textPrint.print("Left Front Button: {}".format( leftBtn1State ) )
        self.textPrint.print("Right Front Button: {}".format( rightBtn1State ) )
        self.textPrint.unindent()
        self.textPrint.print("Front Buttons No.2:" )
        self.textPrint.indent()
        self.textPrint.print("Left Front Button: {}".format( leftBtn2State ) )
        self.textPrint.print("Right Front Button: {}".format( rightBtn2State ) )
        self.textPrint.unindent()
        self.textPrint.print("Other Buttons:" )
        self.textPrint.indent()
        self.textPrint.print("Select Button: {}".format( selectBtnState ) )
        self.textPrint.print("Start Button: {}".format( startBtnState ) )
        self.textPrint.print("Triangle Button: {}".format( triangleBtnState ) )
        self.textPrint.print("Square Button: {}".format( squareBtnState ) )
        self.textPrint.print("Circle Button: {}".format( circleBtnState ) )
        self.textPrint.print("X-cross Button: {}".format( crossXBtnState ) )
        self.textPrint.unindent()
        self.textPrint.print("")
        self.textPrint.print( self.message )
        """
        # Limit to 20 frames per second
        self.clock.tick(20)
        
        # Update the screen 
        pygame.display.flip()

        # Check for quit event
        keepRunning = True
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                keepRunning = False # Flag that we are done so we exit this loop
        
        return keepRunning
    

    def processButton(self, btnIdx, btnName, lastState, btnCallback):
        """Internal function to handle any button press"""
        if btnIdx != -1:
            #Get button value
            btnState = self.controller.get_button( btnIdx )
            #Display value on screen
            self.textPrint.print(btnName + ": {}".format( btnState ) )
            #Call the callback function if defined and button state has changed since last called
            if (btnCallback is not None
            and lastState != btnState ):
                lastState = btnState
                btnCallback( btnState )
        return lastState
    

## --- Test functions for this module below this line ---
def initStatus( status ):
    """Callback function which displays status during initialisation"""
    if status == 0 :
        print("Supported controller connected")
    elif status < 0 :
        print("No supported controller detected")
    else:
        print("Waiting for controller {}".format( status ) )


def leftTrigChangeHandler(val):
    """Callback function which displays the position of the left trigger whenever it changes"""
    print("Left Trigger position changed: {}".format( val ) )
    
    
def leftStickChangeHandler( valLR, valUD ):
    """Callback function which displays the position of the left stick whenever it changes"""
    print("Left Stick position changed: L-R {}, U-D {}".format( valLR, valUD ) )
    
    
def leftBtn1ChangeHandler( val ):
    """Callback function which displays the state of the left front button 1 whenever it changes"""
    print("Left Front Button 1 state: {}".format( val ) )
    
    
def main():
    #Test class
    cnt = RobotController("Game Controller Test", initStatus, leftTriggerChanged = leftTrigChangeHandler,
                          leftStickChanged = leftStickChangeHandler, leftStickPressChanged = leftBtn1ChangeHandler )

    if cnt.initialised :
        keepRunning = True
        
    else:
        keepRunning = False
        
    # -------- Main Program Loop -----------
    while keepRunning == True :
        # Trigger stick events and check for quit
        keepRunning = cnt.controllerStatus()
        
    pygame.quit()


if __name__ == '__main__':
    main()
    