# PiWars2019
Code for my robot entry in the PiWars.org 2019 robotics competition.

This mock branch contains mocked versions of all the hardware interface modules which allows the code to be run and developed on a computer without any of the robot hardware attached. The hardware is simulated in the modules on this branch so that menu and control code can be tested without access to the physical robot. A graphical representation of the robot will be displayed in the application window instead. The code will detect whether it is running on a display the same resolution as the HyperPixel 4 touch screen or not. If the resolution is the same as the Hyperpixel display then the application will run full screen and will run the autonomous code in loops where the screen is only updated every 50 frames. On larger displays the code will run in a window and the graphics will be updated on every cycle (this makes it run a little slow on a Raspberry Pi as the graphics take time to update, but works well on a Linux laptop).

## Installation
To deploy and run this mock robot code follow these steps:

Open a terminal in the location you want to place the code.

Run this command to get the robot controller library used by the project:
> git clone https://github.com/footleg/pygame-controller.git

Run this command to get the master branch of the robot project:
> git clone https://github.com/footleg/PiWars2019.git

Enter the repo directory:
> cd PiWars2019

Run this command to switch to the mock branch:
> git checkout mock

Run the mock robot:
> python3 RockyRover.py

You will need a supported game controller accessible to your computer. Once one is detected the main application window will display the menus. Click on the planets to navigate the menus.

WARNING!!!
The reboot and shutdown menu options on the third level down in the menus will immediately reboot or shutdown your computer with no further warning. Use with care! This is why they are 3 levels down into the menus and the last position you clicked on the screen will correspond to the cancel option on the next level down so you can't accidently tap the same spot on the touchscreen multiple times and shutdown or reboot your computer by mistake.

The controller HAT allows various parameters to be edited on the fly on the robot.
Exit back to the menus from any running mode by either clicking in the 4 quarters of the screen in this order:

```
 1 | 2 
---|---
 3 | 4 
```

or by holding the Select + Start buttons down together on the game controller.

Toggle debug data modes on and off using the controller Home button.

In manual driving mode, spot steering is controlled using the left and right analogue triggers. Drive using the left stick up/down for speed, and the right stick left/right to steer. The front left and right no. 1 buttons activate different levels of power boost for the main motors when held down. You can see the percentage of power the motors are getting if you hold the left stick fully forward and then hold in one, or both of the boost buttons.
