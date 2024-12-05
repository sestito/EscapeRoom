# EscapeRoom
## Software
Requires Python 3! Was coded in Python 3.10.7. Tested in 3.11.3 as well.

Required Packages are: datetime, pyqt6, and pyqt6-tools

## Adjusting the intro video
The intro video was edited with DaVinci Resolve

Adjust the parameters in the config.ini file under the INTRO section for your specific video.

## Adjusting Parameters
Edit all parameters in the config.ini file
* Start time should be when the Escape Room is supposed to start.
* Duration is how many minutes they have to complete the room
* LockoutAttempts is the nubmer of attempts before the program locks them out
* LockoutTime is the number of seconds after LockoutAttempts has been reached
* CodeLength is the maximum length of the code
* Code is the secret code

## Editing the GUI
To install pyQT6
>pip install pyqt6

>pip install pyqt6-tools

To make edits to the GUI, launch with pyqt6-tools designer