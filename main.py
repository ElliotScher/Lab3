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
LIME = Signature(1, -6229, -5727, -5978, -4233, -3815, -4024, 2.5, 0)
LEMON = Signature(2, 1379, 3121, 2250, -3899, -3599, -3749, 2.5, 0)
TANGERINE = Signature(3, 3235, 7503, 5369, -2769, -2331, -2550, 2.5, 0)
GRAPEFRUIT = Signature(4, 5335, 7573, 6454, 941, 1263, 1102, 2.5, 0)

# Defining camera and colors to search for
Vision3 = Vision (Ports.PORT20, 82, TANGERINE, LIME, LEMON, GRAPEFRUIT)

brain.screen.print("Hello V5")

def signatureNameGet(signature: Signature):
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

def snapshotPrint(signature: Signature):
     objects = Vision3.take_snapshot(signature)
     if objects:
        print(signatureNameGet(signature))
        wait(20)

while True:
    snapshotPrint(TANGERINE)


