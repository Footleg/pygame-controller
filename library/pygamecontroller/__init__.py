#!/usr/bin/env python3
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
    """ Provides a Pygame based application to detect controller input
        and interface the controller to your own code.
        
        The constructor takes optional callback functions to be passed
        in which will be called by the RobotController when any buttons,
        control stick or triggers are activated on the game controller.
        Callback functions can also be passed in for mouse events, enabling
        touch screen interfaces to be implemented.
        
        Args:
            title: Will be displayed on the application window title bar
            
            initStatus: A callback function which will be passed integer status values
                during initialisation of the application. The function given as this argument
                will be called while the application is detecting a supported game controller.
                A status code of 0 indicates a controller was successfully detected.
                Status codes in the range 1 - 32 indicate attempts to detect a controller. While
                these values are being returned, the application is waiting for a controller to
                be connected (via cable or bluetooth). The status value indicates how many
                attempts have been made. After 32 attempts if no supported controller has been
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
                the 4-way hat as a pair of integers representing the Left/Right and Up/Down states of the
                hat buttons. The Left/Right state = -1 for left, 0 for centre and 1 for right. The Up/Down
                state = 1 for up, 0 for centre and -1 for down. This function will only be called when the 
                hat state changes, so your application code will only be called when something needs
                to be updated.
            
            leftStickPressChanged: A callback function for the left stick pressed state (see leftBtn1Changed)
            
            rightStickPressChanged: A callback function for the right stick pressed state (see leftBtn1Changed)
            
            selectBtnChanged: A callback function for the Select button (see leftBtn1Changed)
            
            homeBtnChanged: A callback function for the Home button (see leftBtn1Changed)
            
            startBtnChanged: A callback function for the Start button (see leftBtn1Changed)
            
            starBtnChanged: A callback function for the Star button (see leftBtn1Changed)
            
            triangleBtnChanged: A callback function for the triangle symbol button (see leftBtn1Changed)
            
            squareBtnChanged: A callback function for the square symbol button (see leftBtn1Changed)
            
            circleBtnChanged: A callback function for the circle symbol button (see leftBtn1Changed)
            
            crossXBtnChanged: A callback function for the X symbol button (see leftBtn1Changed)
            
            mouseDown: A callback function which returns the position of the mouse and the button pressed down 
            
            mouseUp: A callback function which returns the position of the mouse and the button released 
                
        """
    
    # Names for supported controllers. These are the names the controllers present themselves as.
    SUPPORTED_JOYSTICKS = ("PLAYSTATION(R)3",
                           "Rock Candy Wireless Gamepad for PS3",
                           "hongjingda HJD-X",
                           "PS3/USB Corded Gamepad",
                           "Wireless Controller",
                           "8BitDo Pro 2",
                           "Xbox One S",
                           "Pro Controller",
                           "Logitech Gamepad F710")
    DETECTED_JOYSTICK_IDX = -1
    
    #Define specifications of each supported controller
    AXES = (
        27, # PS3 Dualshock
        4,  # Rock Candy USB Dongle
        6,  # Pi Hut USB Dongle
        4,  # Argos PS3 compatible
        6,  # PS4 Dualshock Wireless
        6,  # 8BitDo Pro 2 (D mode)
        6,  # 8BitDo Pro 2 (X mode)
        4,  # 8BitDo Pro 2 (S mode)
        6,  # Logitech Gamepad F710
    )
    
    BTNS = (
        19, # PS3 Dualshock
        13, # Rock Candy USB Dongle
        15, # Pi Hut USB Dongle
        12, # Argos PS3 compatible
        13, # PS4 Dualshock Wireless
        16, # 8BitDo Pro 2 (D mode)
        11, # 8BitDo Pro 2 (X mode)
        16, # 8BitDo Pro 2 (S mode)
        11, # Logitech Gamepad F710
    )

    HATS = (
        0, # PS3 Dualshock
        1, # Rock Candy USB Dongle
        1, # Pi Hut USB Dongle
        1, # Argos PS3 compatible
        1, # PS4 Dualshock Wireless
        1, # 8BitDo Pro 2 (D mode)
        1, # 8BitDo Pro 2 (X mode)
        1, # 8BitDo Pro 2 (S mode)
        1, # Logitech Gamepad F710

    )
    
    '''
        , # PS3 Dualshock
        , # Rock Candy USB Dongle
        , # Pi Hut USB Dongle
        , # Argos PS3 compatible
        , # PS4 Dualshock Wireless
        , # 8BitDo Pro 2 (D mode)
        , # 8BitDo Pro 2 (X mode)
        , # 8BitDo Pro 2 (S mode)
    )

    '''

    CONTROLLER_DISPLAY_NAMES = ("Sony PS3 Dualshock 6-axis Controller",
                                "Rock Candy Wireless Gamepad for PS3",
                                "ThePiHut Wiresless USB Game Controller",
                                "Argos PS3 Compatible Gamepad",
                                "Sony PS4 Wireless Controller",
                                "8BitDo Pro 2 (S Mode)",
                                "XBox One S",
                                "8BitDo Pro 2 (S Mode)",
                                "Logitech Gamepad F710")
    
    ## Define indices for each control for the different supported controllers
    
    # Axes
    leftTriggerIdx = (
        12, # PS3 Dualshock
        -1, # Rock Candy USB Dongle
        4,  # Pi Hut USB Dongle
        -1, # Argos PS3 compatible
        2,  # PS4 Dualshock Wireless
        5,  # 8BitDo Pro 2 (D mode)
        2,  # 8BitDo Pro 2 (X mode)
        -1, # 8BitDo Pro 2 (S mode)
        2, # Logitech Gamepad F710
    )
    
    rightTriggerIdx = (
        13, # PS3 Dualshock
        -1, # Rock Candy USB Dongle
        5,  # Pi Hut USB Dongle
        -1, # Argos PS3 compatible
        5,  # PS4 Dualshock Wireless
        4,  # 8BitDo Pro 2 (D mode)
        5,  # 8BitDo Pro 2 (X mode)
        -1, # 8BitDo Pro 2 (S mode)
        5, # Logitech Gamepad F710
    )
    
    leftStickLRIdx = (
        0, # PS3 Dualshock
        0, # Rock Candy USB Dongle
        0, # Pi Hut USB Dongle
        0, # Argos PS3 compatible
        0, # PS4 Dualshock Wireless
        0, # 8BitDo Pro 2 (D mode)
        0, # 8BitDo Pro 2 (X mode)
        0, # 8BitDo Pro 2 (S mode)
        0, # Logitech Gamepad F710
    )
    
    leftStickUDIdx = (
        1, # PS3 Dualshock
        1, # Rock Candy USB Dongle
        1, # Pi Hut USB Dongle
        1, # Argos PS3 compatible
        1, # PS4 Dualshock Wireless
        1, # 8BitDo Pro 2 (D mode)
        1, # 8BitDo Pro 2 (X mode)
        1, # 8BitDo Pro 2 (S mode)
        1, # Logitech Gamepad F710
    )
    
    rightStickLRIdx = (
        2, # PS3 Dualshock
        2, # Rock Candy USB Dongle
        2, # Pi Hut USB Dongle
        2, # Argos PS3 compatible
        3, # PS4 Dualshock Wireless
        2, # 8BitDo Pro 2 (D mode)
        3, # 8BitDo Pro 2 (X mode)
        2, # 8BitDo Pro 2 (S mode)
        3, # Logitech Gamepad F710
    )
    
    rightStickUDIdx = (
        3, # PS3 Dualshock
        3, # Rock Candy USB Dongle
        3, # Pi Hut USB Dongle
        3, # Argos PS3 compatible
        4, # PS4 Dualshock Wireless
        3, # 8BitDo Pro 2 (D mode)
        4, # 8BitDo Pro 2 (X mode)
        3, # 8BitDo Pro 2 (S mode)
        4, # Logitech Gamepad F710
    )
    
    # Buttons
    leftBtn1Idx = (
        10, # PS3 Dualshock
         4, # Rock Candy USB Dongle
         6, # Pi Hut USB Dongle
         4, # Argos PS3 compatible
         4, # PS4 Dualshock Wireless
         6, # 8BitDo Pro 2 (D mode)
         4, # 8BitDo Pro 2 (X mode)
         4, # 8BitDo Pro 2 (S mode)
         4, # Logitech Gamepad F710
    )
    
    rightBtn1Idx = (
        11, # PS3 Dualshock
         5, # Rock Candy USB Dongle
         7, # Pi Hut USB Dongle
         5, # Argos PS3 compatible
         5, # PS4 Dualshock Wireless
         7, # 8BitDo Pro 2 (D mode)
         5, # 8BitDo Pro 2 (X mode)
         5, # 8BitDo Pro 2 (S mode)
         5, # Logitech Gamepad F710
    )
    
    leftBtn2Idx = (
         8, # PS3 Dualshock
         6, # Rock Candy USB Dongle
         8, # Pi Hut USB Dongle
         6, # Argos PS3 compatible
         6, # PS4 Dualshock Wireless
         8, # 8BitDo Pro 2 (D mode)
        -1, # 8BitDo Pro 2 (X mode)
         6, # 8BitDo Pro 2 (S mode)
        -1, # Logitech Gamepad F710
    )
    
    rightBtn2Idx = (
         9, # PS3 Dualshock
         7, # Rock Candy USB Dongle
         9, # Pi Hut USB Dongle
         7, # Argos PS3 compatible
         7, # PS4 Dualshock Wireless
         9, # 8BitDo Pro 2 (D mode)
        -1, # 8BitDo Pro 2 (X mode)
         7, # 8BitDo Pro 2 (S mode)
        -1, # Logitech Gamepad F710
    )
    
    leftStickPressIdx = (
         1, # PS3 Dualshock
        10, # Rock Candy USB Dongle
        13, # Pi Hut USB Dongle
        10, # Argos PS3 compatible
        11, # PS4 Dualshock Wireless
        13, # 8BitDo Pro 2 (D mode)
         8, # 8BitDo Pro 2 (X mode)
        10, # 8BitDo Pro 2 (S mode)
         9, # Logitech Gamepad F710
    )
    
    rightStickPressIdx = (
         2, # PS3 Dualshock
        11, # Rock Candy USB Dongle
        14, # Pi Hut USB Dongle
        11, # Argos PS3 compatible
        12, # PS4 Dualshock Wireless
        14, # 8BitDo Pro 2 (D mode)
         9, # 8BitDo Pro 2 (X mode)
        11, # 8BitDo Pro 2 (S mode)
        10, # Logitech Gamepad F710
    )
    
    triangleXBtnIdx = (
        12, # PS3 Dualshock
         3, # Rock Candy USB Dongle
         4, # Pi Hut USB Dongle
         0, # Argos PS3 compatible
         2, # PS4 Dualshock Wireless
         3, # 8BitDo Pro 2 (D mode)
         3, # 8BitDo Pro 2 (X mode)
         3, # 8BitDo Pro 2 (S mode)
         3, # Logitech Gamepad F710  (labelled Y)
    )
    
    squareYBtnIdx = (
        15, # PS3 Dualshock
         0, # Rock Candy USB Dongle
         3, # Pi Hut USB Dongle
         3, # Argos PS3 compatible
         3, # PS4 Dualshock Wireless
         4, # 8BitDo Pro 2 (D mode)
         2, # 8BitDo Pro 2 (X mode)
         2, # 8BitDo Pro 2 (S mode)
         2, # Logitech Gamepad F710  (labelled X)
    )
    
    circleABtnIdx = (
        13, # PS3 Dualshock
         2, # Rock Candy USB Dongle
         1, # Pi Hut USB Dongle
         1, # Argos PS3 compatible
         1, # PS4 Dualshock Wireless
         0, # 8BitDo Pro 2 (D mode)
         1, # 8BitDo Pro 2 (X mode)
         1, # 8BitDo Pro 2 (S mode)
         1, # Logitech Gamepad F710  (labelled B)
    )
    
    crossBBtnIdx = (
        14, # PS3 Dualshock
         1, # Rock Candy USB Dongle
         0, # Pi Hut USB Dongle
         2, # Argos PS3 compatible
         0, # PS4 Dualshock Wireless
         1, # 8BitDo Pro 2 (D mode)
         0, # 8BitDo Pro 2 (X mode)
         0, # 8BitDo Pro 2 (S mode)
         0, # Logitech Gamepad F710  (labelled A)
    )
    
    selectBtnIdx = (
         0, # PS3 Dualshock
         8, # Rock Candy USB Dongle
        10, # Pi Hut USB Dongle
         8, # Argos PS3 compatible
         9, # PS4 Dualshock Wireless
        10, # 8BitDo Pro 2 (D mode)
         6, # 8BitDo Pro 2 (X mode)
         8, # 8BitDo Pro 2 (S mode)
         6, # Logitech Gamepad F710 (labelled Back)
    )
    
    homeBtnIdx = (
        16, # PS3 Dualshock
        12, # Rock Candy USB Dongle
        12, # Pi Hut USB Dongle
        -1, # Argos PS3 compatible
        10, # PS4 Dualshock Wireless
        12, # 8BitDo Pro 2 (D mode)
        10, # 8BitDo Pro 2 (X mode)
        12, # 8BitDo Pro 2 (S mode)
         8, # Logitech Gamepad F710
    )
    
    startBtnIdx = (
         3, # PS3 Dualshock
         9, # Rock Candy USB Dongle
        11, # Pi Hut USB Dongle
         9, # Argos PS3 compatible
         8, # PS4 Dualshock Wireless
        11, # 8BitDo Pro 2 (D mode)
         7, # 8BitDo Pro 2 (X mode)
         9, # 8BitDo Pro 2 (S mode)
         7, # Logitech Gamepad F710
    )
    
    starBtnIdx = (
        -1, # PS3 Dualshock
        -1, # Rock Candy USB Dongle
        -1, # Pi Hut USB Dongle
        -1, # Argos PS3 compatible
        -1, # PS4 Dualshock Wireless
        -1, # 8BitDo Pro 2 (D mode)
        -1, # 8BitDo Pro 2 (X mode)
        13, # 8BitDo Pro 2 (S mode)
        -1, # Logitech Gamepad F710
    )

    
    # Hats which manifest as separate buttons
    hatLeftIdx = (
         7, # PS3 Dualshock
        -1, # Rock Candy USB Dongle
        -1, # Pi Hut USB Dongle
        -1, # Argos PS3 compatible
        -1, # PS4 Dualshock Wireless
        -1, # 8BitDo Pro 2 (D mode)
        -1, # 8BitDo Pro 2 (X mode)
        -1, # 8BitDo Pro 2 (S mode)
    )
    
    hatRightIdx = (
         5, # PS3 Dualshock
        -1, # Rock Candy USB Dongle
        -1, # Pi Hut USB Dongle
        -1, # Argos PS3 compatible
        -1, # PS4 Dualshock Wireless
        -1, # 8BitDo Pro 2 (D mode)
        -1, # 8BitDo Pro 2 (X mode)
        -1, # 8BitDo Pro 2 (S mode)
        -1, # Logitech Gamepad F710
    )
    
    hatUpIdx = (
         4, # PS3 Dualshock
        -1, # Rock Candy USB Dongle
        -1, # Pi Hut USB Dongle
        -1, # Argos PS3 compatible
        -1, # PS4 Dualshock Wireless
        -1, # 8BitDo Pro 2 (D mode)
        -1, # 8BitDo Pro 2 (X mode)
        -1, # 8BitDo Pro 2 (S mode)
        -1, # Logitech Gamepad F710
    )
    
    hatDownIdx = (
         6, # PS3 Dualshock
        -1, # Rock Candy USB Dongle
        -1, # Pi Hut USB Dongle
        -1, # Argos PS3 compatible
        -1, # PS4 Dualshock Wireless
        -1, # 8BitDo Pro 2 (D mode)
        -1, # 8BitDo Pro 2 (X mode)
        -1, # 8BitDo Pro 2 (S mode)
        -1, # Logitech Gamepad F710
    )
    
    
    # True hats
    hatIdx = (
        -1, # PS3 Dualshock
         0, # Rock Candy USB Dongle
         0, # Pi Hut USB Dongle
         0, # Argos PS3 compatible
         0, # PS4 Dualshock Wireless
         0, # 8BitDo Pro 2 (D mode)
         0, # 8BitDo Pro 2 (X mode)
         0, # 8BitDo Pro 2 (S mode)
        -1, # Logitech Gamepad F710
    )
    

    #Properties holding program status or controlling behaviour
    initialised = False
    displayControllerOutput = True
    
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
    homeBtnState = 0
    startBtnState = 0
    starBtnState = 0
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
                 selectBtnChanged = None, homeBtnChanged = None, startBtnChanged = None, starBtnChanged = None, triangleBtnChanged = None,
                 squareBtnChanged = None, circleBtnChanged = None, crossXBtnChanged = None,
                 mouseDown = None, mouseUp = None):
        
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
        self.homeBtnChanged = homeBtnChanged
        self.startBtnChanged = startBtnChanged
        self.starBtnChanged = starBtnChanged
        self.triangleBtnChanged = triangleBtnChanged
        self.squareBtnChanged = squareBtnChanged
        self.circleBtnChanged = circleBtnChanged
        self.crossXBtnChanged = crossXBtnChanged
        self.mouseDown = mouseDown
        self.mouseUp = mouseUp
        
        #Look for supported game controller
        controllerFound = False
        lastCount = 0
        for retries in range(1, 33):
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
                    print("Joystick {} detected as ".format(i) + name )
                    
                    #Determine whether detected joystick is a supported model type 
                    for j in range(0, len(self.SUPPORTED_JOYSTICKS) ) :
                        #Looking for the supporter name text as a substring of the detected full name
                        if self.SUPPORTED_JOYSTICKS[j] in name:
                            self.DETECTED_JOYSTICK_IDX = j
                            break
                                    
                    if self.DETECTED_JOYSTICK_IDX > -1 :
                        #Check the controller matches the expected specifications
                        axes = joystick.get_numaxes()
                        if axes == self.AXES[self.DETECTED_JOYSTICK_IDX] :
                            hats = joystick.get_numhats()
                            if hats == self.HATS[self.DETECTED_JOYSTICK_IDX] :
                                btns = joystick.get_numbuttons()
                                if btns >= self.BTNS[self.DETECTED_JOYSTICK_IDX] :
                                    #Set up this controller
                                    self.controller = joystick
                                    controllerFound = True
                                    
                                    #Send status success to callback function
                                    self.initStatus(0)
                                    break
                                else:
                                    print("Joystick has {} buttons. Expected at least {}.".format( btns,self.BTNS[self.DETECTED_JOYSTICK_IDX] ) )
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
            size = [400, 500]
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
        if self.displayControllerOutput == True:
            self.textPrint.reset()
            self.textPrint.print("Controller: {}".format( self.CONTROLLER_DISPLAY_NAMES[self.DETECTED_JOYSTICK_IDX] ) )
            self.textPrint.indent()
        
        #Process analogue sticks
        if (self.leftStickLRIdx[self.DETECTED_JOYSTICK_IDX] != -1
        and self.leftStickUDIdx[self.DETECTED_JOYSTICK_IDX] != -1 ):
            #Get stick postitions
            leftStickLR = self.controller.get_axis( self.leftStickLRIdx[self.DETECTED_JOYSTICK_IDX] )
            leftStickUD = self.controller.get_axis( self.leftStickUDIdx[self.DETECTED_JOYSTICK_IDX] )

            if self.displayControllerOutput == True:
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
            if self.displayControllerOutput == True:
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
        if self.displayControllerOutput == True:
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
            if self.displayControllerOutput == True:
                #Display value on screen
                self.textPrint.print("Left Trigger: {}".format( leftTrigger ) )
            #Call the callback function if defined and trigger position has changed since last called
            if (self.leftTriggerChanged is not None
            and self.leftTriggerActivated == True
            and self.leftTriggerPos != leftTrigger ):
                self.leftTriggerPos = leftTrigger
                self.leftTriggerChanged( self.leftTriggerPos )
        elif self.displayControllerOutput == True:
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
            if self.displayControllerOutput == True:
                #Display value on screen
                self.textPrint.print("Right Trigger: {}".format( rightTrigger ) )
                self.textPrint.unindent()
            #Call the callback function if defined and trigger position has changed since last called
            if (self.rightTriggerChanged is not None
            and self.rightTriggerActivated == True
            and self.rightTriggerPos != rightTrigger ):
                self.rightTriggerPos = rightTrigger
                self.rightTriggerChanged( self.rightTriggerPos )
        elif self.displayControllerOutput == True:
            self.textPrint.print("No analogue Right Trigger on this controller" )
            self.textPrint.unindent()
        
        #Process Hats
        if self.hatIdx[self.DETECTED_JOYSTICK_IDX] != -1:
            hatState = self.controller.get_hat( self.hatIdx[self.DETECTED_JOYSTICK_IDX] )
            hatLR = hatState[0]
            hatUD = hatState[1]
            if self.displayControllerOutput == True:
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
            if self.displayControllerOutput == True:
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
            self.hatChanged( self.hatLRState, self.hatUDState )
        
        #Process buttons
        if self.displayControllerOutput == True:
            self.textPrint.print("Simple buttons:" )
            self.textPrint.indent()

        self.leftBtn1State = self.processButton(
            self.leftBtn1Idx[self.DETECTED_JOYSTICK_IDX],
            "Left Trigger Button 1", self.leftBtn1State, self.leftBtn1Changed)
        self.rightBtn1State = self.processButton(
            self.rightBtn1Idx[self.DETECTED_JOYSTICK_IDX],
            "Right Trigger Button 1", self.rightBtn1State, self.rightBtn1Changed)
        if self.leftTriggerIdx[self.DETECTED_JOYSTICK_IDX] == -1 :
            #No analogue trigger so handle as simple button
            self.leftBtn2State = self.processButton(
                self.leftBtn2Idx[self.DETECTED_JOYSTICK_IDX],
                "Left Trigger Button 2", self.leftBtn2State, self.leftBtn2Changed)
        if self.rightTriggerIdx[self.DETECTED_JOYSTICK_IDX] == -1 :
            #No analogue trigger so handle as simple button
            self.rightBtn2State = self.processButton(
                self.rightBtn2Idx[self.DETECTED_JOYSTICK_IDX],
                "Right Trigger Button 2", self.rightBtn2State, self.rightBtn2Changed)
        
        self.leftStickPressedState = self.processButton(
            self.leftStickPressIdx[self.DETECTED_JOYSTICK_IDX],
            "Left Stick Pressed", self.leftStickPressedState, self.leftStickPressChanged)
        self.rightStickPressedState = self.processButton(
            self.rightStickPressIdx[self.DETECTED_JOYSTICK_IDX],
            "Right Stick Pressed", self.rightStickPressedState, self.rightStickPressChanged)

        self.selectBtnState = self.processButton(
            self.selectBtnIdx[self.DETECTED_JOYSTICK_IDX],
            "Select Button", self.selectBtnState, self.selectBtnChanged)
        self.homeBtnState = self.processButton(
            self.homeBtnIdx[self.DETECTED_JOYSTICK_IDX],
            "Home Button", self.homeBtnState, self.homeBtnChanged)
        self.startBtnState = self.processButton(
            self.startBtnIdx[self.DETECTED_JOYSTICK_IDX],
            "Start Button", self.startBtnState, self.startBtnChanged)
        self.starBtnState = self.processButton(
            self.starBtnIdx[self.DETECTED_JOYSTICK_IDX],
            "Star Button", self.starBtnState, self.starBtnChanged)

        
        self.triangleBtnState = self.processButton(
            self.triangleXBtnIdx[self.DETECTED_JOYSTICK_IDX],
            "Triangle Button", self.triangleBtnState, self.triangleBtnChanged)
        self.squareBtnState = self.processButton(
            self.squareYBtnIdx[self.DETECTED_JOYSTICK_IDX],
            "Square Button", self.squareBtnState, self.squareBtnChanged)
        self.circleBtnState = self.processButton(
            self.circleABtnIdx[self.DETECTED_JOYSTICK_IDX],
            "Circle Button", self.circleBtnState, self.circleBtnChanged)
        self.crossXBtnState = self.processButton(
            self.crossBBtnIdx[self.DETECTED_JOYSTICK_IDX],
            "X-Cross Button", self.crossXBtnState, self.crossXBtnChanged)

        if self.displayControllerOutput == True:
            #Display any message text set outside the class
            self.textPrint.unindent()
            self.textPrint.print("")
            self.textPrint.print( self.message )
        
        # Limit to 20 frames per second
        self.clock.tick(20)
        
        # Update the screen 
        pygame.display.flip()

        # Check for quit event
        keepRunning = True
        for event in pygame.event.get(): # User did something
            if ( (event.type == pygame.MOUSEBUTTONDOWN)
            and (self.mouseDown is not None) ):
                self.mouseDown( pygame.mouse.get_pos(), event.button )
            elif event.type == pygame.QUIT: # If user clicked close
                keepRunning = False # Flag that we are done so we exit this loop
        
        return keepRunning
    

    def processButton(self, btnIdx, btnName, lastState, btnCallback):
        """Internal function to handle any button press"""
        if btnIdx != -1:
            #Get button value
            btnState = self.controller.get_button( btnIdx )
            if self.displayControllerOutput == True:
                #Display value on screen
                self.textPrint.print(btnName + ": {}".format( btnState ) )
            #Call the callback function if defined and button state has changed since last called
            if (btnCallback is not None
            and lastState != btnState ):
                lastState = btnState
                btnCallback( btnState )
        return lastState
    

## --- Test functions for this module below this line ---
def initStatusHandler( status ):
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
    rc = RobotController("Game Controller Test", initStatusHandler, leftTriggerChanged = leftTrigChangeHandler,
                          leftStickChanged = leftStickChangeHandler, leftStickPressChanged = leftBtn1ChangeHandler )

    if rc.initialised :
        keepRunning = True
        
    else:
        keepRunning = False
        
    # -------- Main Program Loop -----------
    while keepRunning == True :
        # Trigger stick events and check for quit
        keepRunning = rc.controllerStatus()
        
    pygame.quit()


if __name__ == '__main__':
    main()
    
