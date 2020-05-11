# Pygame Controller
This project is designed to make it simple to add game controllers to python programs for controlling attached hardware. It consists of a class which maps game controllers to your own code functions and some examples and a template file to help you get started. The original design was created to assist controlling Raspberry Pi based robots using game controllers so that people learning python on Raspberry Pi computers could easily get started in mapping the joysticks, triggers and buttons on a game controller to motors, servos and lights. 

## Controller Support
This project currently supports the following controllers:
* Sony PS3 Dualshock Wireless controller
* Sony PS4 Wireless Controller
* The Pi Hut wireless USB game controller
* Rock Candy wireless USB game controller
* Generic wireless USB game controller from Argos

## Usage and Examples
There are some common problems in interfacing code to game controllers as inputs which Pygame Controller provides solutions to. 
* Different models of game controller send different information for the same controls. One might map the home button to button number 16 in the array of detected buttons, while another might map it to number 12. Pygame Controller enables the same code to respond to the user pressing a particular button, trigger or joystick regardless of which of the supported controllers is connected.
* It is not always efficient to continually update outputs from your program to control hardware when there has been no change in the state of the control position which is mapped to that output. Pygame Controller only calls your code functions when the value of the control mapped to that code actually changes. e.g. If a button is pressed and held down then the code linked to that button will only be called once when the button is pressed, and not continually called in a loop. The code linked to the control will only be called again when the button is released.
* When booting up the Raspberry Pi with your program configured to launch automatically and you are using a wireless bluetooth game controller, you need time to pair the controller with the pi before the program can use it. Pygame Controller provides a way to indicate that the computer OS has booted up and the program is waiting for the controller to be paired before it tries to use the controller. This enables you to provide feedback via your hardware to tell the user the status when no monitor is attached. e.g. A robot with LEDs can indicate that it is waiting for a controller to be paired, or that it has been paired successfully, or failed to be detected. By using the initialisation status callback to display information via the LEDs the user can be given feedback. See the Blinkt Controller example /examples/Blinkt/BlinktController.py on github for an example of how this can be done.

As the name suggests, Pygame Controller is based on the Pygame engine. This means it creates a user interface which is displayed on a desktop. The application window displays the state of all the controls on the game controller, and can also be used to display additional messages from your program code. This aids in learning how the controller works, and in debugging what your program is doing.
