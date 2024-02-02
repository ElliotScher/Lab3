# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       cdbrant                                                      #
# 	Created:      9/11/2023, 8:28:37 AM                                        #
# 	Description:  Confusion matrix                                             #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

button5 = Bumper(Ports.PORT5)

# Defining color signatures
LIME = Signature(1, -6709, -5251, -5980, -3811, -2963, -3387, 3.6, 0)
LEMON = Signature(2, 1351, 2689, 2020, -3715, -3343, -3529, 2.5, 0)
TANGERINE = Signature(3, 2105, 7635, 4870, -2561, -2059, -2310, 2.5, 0)
GRAPEFRUIT = Signature(4, 2871, 6991, 4931, 1081, 1531, 1306, 2.5, 0)

# Defining camera and colors to search for
Vision3 = Vision (Ports.PORT3, 72, TANGERINE, LIME, LEMON, GRAPEFRUIT)

brain.screen.print("Hello V5")

ROBOT_IDLE = 0
ROBOT_SEARCHING = 1

# Starts in the idle state
state = ROBOT_IDLE

def getSignatureName(id):
    if id == 1:
        return "LIME"
    elif id == 2:
        return "LEMON"
    elif id == 3:
        return "TANGERINE"
    elif id == 4:
        return "GRAPEFRUIT"
    else:
        return "ERROR"

def handleButtonPress():
    global state
    if(state == ROBOT_IDLE):
        print('Parsing color')
        state = ROBOT_SEARCHING
        

    else:
        print('Waiting')
        
button5.pressed(handleButtonPress)
objects = Vision3.take_snapshot(TANGERINE)
print(str(objects))