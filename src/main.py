# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Elliot Scher                                                 #
# 	Created:      1/31/2024, 7:59:50 AM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()

# Define vision signatures
LIME = Signature(1, -6709, -5251, -5980, -3811, -2963, -3387, 2.5, 0)
LEMON = Signature(2, 1351, 2689, 2020, -3715, -3343, -3529, 2.5, 0)
TANGERINE = Signature(3, 2105, 7635, 4870, -2561, -2059, -2310, 2.5, 0)
GRAPEFRUIT = Signature(4, 2871, 6991, 4931, 1081, 1531, 1306, 2.5, 0)

vision = Vision(Ports.PORT20, 82, LIME, LEMON, TANGERINE, GRAPEFRUIT)

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

FRUIT_HEIGHT_IN = 3

# at a distance of 12 inches, the target was 142 pixels tall
CALIBRATION_DISTANCE_IN = 12
CALIBRATION_HEIGHT_PX = 64

def findSignatureDistance(height: float):
    return (FRUIT_HEIGHT_IN / 2) / math.atan(math.tan((FRUIT_HEIGHT_IN / 2) / CALIBRATION_DISTANCE_IN) * height / CALIBRATION_HEIGHT_PX)

X_FOV = 61

def findXOffsetDegrees(x: float):
    return (160 - x) / 320 * X_FOV

def printSnapshot(signature: Signature):
    objects = vision.take_snapshot(signature)  
    if objects:
        print("sig: " + getSignatureName(signature), "deg: " + str(findXOffsetDegrees(vision.largest_object().centerX)), "dist: " + str(findSignatureDistance(vision.largest_object().height)))  
    else:
        print("No " + getSignatureName(signature))
    wait(20)

while True:
    printSnapshot(LIME)
    # printSnapshot(LEMON)
    # printSnapshot(TANGERINE)
    # printSnapshot(GRAPEFRUIT)