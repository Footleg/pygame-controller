# Pygame Controller
This project is designed to make it simple to add game controllers to python programs for controlling attached hardware. It consists of a class which maps game controllers to your own code functions and some examples and a template file to help you get started. The original design was created to assist controlling Raspberry Pi based robots using game controllers so that people learning python on Raspberry Pi computers could easily get started in mapping the joysticks, triggers and buttons on a game controller to motors, servos and lights. It has since been proven as a controller library in the prestigious Pi Wars robot competition to produce a remote controlled robot with a full GUI (see my [Pi Wars 2019](https://github.com/Footleg/PiWars2019) github repository for details).

## Installation
Pygame Controller is now available on PyPi. So you can install or upgrade the package using pip:
```bash
pip3 install --upgrade pygame-controller
```
To deploy the examples, clone this git repo to your Raspberry Pi:
```bash
git clone https://github.com/Footleg/pygame-controller
```
### Install from source
If you just want the latest stable release, then you can use pip3 as detailed above.
If you want to build the latest source, or build from another branch, you can build 
the library package using setup tools:
```bash
cd pygame-controller
sudo python3 setup.py install
```
## Controller Support
This project currently supports the following controllers:
* Sony PS3 Dualshock Wireless controller
* Sony PS4 Wireless controller (and compatibles)
* 8BitDo Pro 2 controller
* The Pi Hut wireless USB game controller
* Rock Candy wireless USB game controller
* Generic wireless USB game controller from Argos

## Usage and Examples
There are some common problems in interfacing code to game controllers as inputs which Pygame Controller provides solutions to. 
* Different models of game controller send different information for the same controls. One might map the home button to button number 16 in the array of detected buttons, while another might map it to number 12. Pygame Controller enables the same code to respond to the user pressing a particular button, trigger or joystick regardless of which of the supported controllers is connected.
* It is not always efficient to continually update outputs from your program to control hardware when there has been no change in the state of the control position which is mapped to that output. Pygame Controller only calls your code functions when the value of the control mapped to that code actually changes. e.g. If a button is pressed and held down then the code linked to that button will only be called once when the button is pressed, and not continually called in a loop. The code linked to the control will only be called again when the button is released.
* When booting up the Raspberry Pi with your program configured to launch automatically and you are using a wireless bluetooth game controller, you need time to pair the controller with the pi before the program can use it. Pygame Controller provides a way to indicate that the computer OS has booted up and the program is waiting for the controller to be paired before it tries to use the controller. This enables you to provide feedback via your hardware to tell the user the status when no monitor is attached. e.g. A robot with LEDs can indicate that it is waiting for a controller to be paired, or that it has been paired successfully, or failed to be detected. By using the initialisation status callback to display information via the LEDs the user can be given feedback. See the [Blinkt Controller example](https://github.com/Footleg/pygame-controller/tree/master/examples/Blinkt/BlinktController.py) for an example of how this can be done.

As the name suggests, Pygame Controller is based on the Pygame engine. This means it creates a user interface which is displayed on a desktop. The application window displays the state of all the controls on the game controller, and can also be used to display additional messages from your program code. This aids in learning how the controller works, and in debugging what your program is doing.

For a high performance robot you may not want the overhead of running your program on a full desktop with a windowed application, in which case Pygame Controller may not be the right project for you. You might find the [approxeng.input library](https://approxeng.github.io/approxeng.input/) more suitable. Pygame Controller works well for simple robots controlling just a few motors and servos, or if you want visual feedback on screen to help teach, or to help yourself learn. It is a great library for building robots with graphical on screen display interfaces or touch screen menus (see my [Pi Wars 2019](https://github.com/Footleg/PiWars2019) github repository for an example using a Pimoroni Hyperpixel Touch display).

To help you start writing your own programs based on Pygame Controller, a [template project file](https://github.com/Footleg/pygame-controller/tree/master/examples/template.py) is provided. For examples using various different HATs take a look in the [examples](https://github.com/Footleg/pygame-controller/tree/master/examples) folder.
