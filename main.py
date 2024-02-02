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

button5 = Bumper(brain.three_wire_port.e)

# Defining color signatures
LIME = Signature(1, -6709, -5251, -5980, -3811, -2963, -3387, 3.6, 0)
LEMON = Signature(2, 1351, 2689, 2020, -3715, -3343, -3529, 2.5, 0)
TANGERINE = Signature(3, 2105, 7635, 4870, -2561, -2059, -2310, 2.5, 0)
GRAPEFRUIT = Signature(4, 2871, 6991, 4931, 1081, 1531, 1306, 2.5, 0)

# Defining camera and colors to search for
Vision3 = Vision (Ports.PORT20, 82, TANGERINE, LIME, LEMON, GRAPEFRUIT)

brain.screen.print("Hello V5")

def getSignatureName(signature: Signature):
    if signature == LIME:
        return "LIME"
    elif signature == LEMON:
        return "LEMON"
    elif signature == TANGERINE:
        return "TANGERINE"
    elif signature == GRAPEFRUIT:
        return "GRAPEFRUIT"
    else:
        return "ERROR"

def printSnapshot(signature: Signature):
    while True:
     objects = Vision3.take_snapshot(TANGERINE)
     if objects:
        print(getSignatureName(signature))
        wait(20)

printSnapshot(TANGERINE)


