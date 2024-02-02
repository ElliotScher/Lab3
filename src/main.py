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

SIGNATURE_SELECTIVITY = 2.5

# Define vision signatures
LIME = Signature(1, -6229, -5727, -5978, -4233, -3815, -4024, SIGNATURE_SELECTIVITY, 0)
LEMON = Signature(2, 1379, 3121, 2250, -3899, -3599, -3749, SIGNATURE_SELECTIVITY, 0)
TANGERINE = Signature(3, 3235, 7503, 5369, -2769, -2331, -2550, SIGNATURE_SELECTIVITY, 0)
GRAPEFRUIT = Signature(4, 5335, 7573, 6454, 941, 1263, 1102, SIGNATURE_SELECTIVITY, 0)

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