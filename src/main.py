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
LIME = Signature (1, -5461, -4635, -5048, -3641, -3071, -3356, 4.5, 0)
LEMON = Signature (2, -49, 151, 51, -3407, -2521, -2964, 5.5, 0)
TANGERINE = Signature (3, 1121, 3095, 2108, -2765, -2405, -2585, 5.5, 0)
GRAPEFRUIT = Signature (4, 2469, 4465, 3467, 1111, 1439, 1275, 2.5, 0)

vision = Vision(Ports.PORT20, 50, LIME, LEMON, TANGERINE, GRAPEFRUIT)

button = Bumper(brain.three_wire_port.e)

leftDrive = Motor(Ports.PORT1, True)
rightDrive = Motor(Ports.PORT10)
arm = Motor(Ports.PORT7)

TARGET_FRUIT = LEMON
TARGET_DISTANCE_IN = 4
TARGET_MAX_DISTANCE_IN = 18

WHEEL_DIAMETER_IN = 4
WHEEL_BASE_IN = 11.625
GEAR_RATIO = 4

FOLLOW_SPEED_M_PER_S = 0.2
FIND_SPEED_RAD_PER_S = math.pi / 8

ROTATE_KP = 1.5

ARM_TOUCH_FRUIT_ANGLE_DEG = -50

IDLE_STATE = 0
FOLLOW_STATE = 1
TOUCH_STATE = 2

state = IDLE_STATE

leftDrive.reset_position()
rightDrive.reset_position()
arm.reset_position()

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
CALIBRATION_HEIGHT_PX = 65

def findSignatureDistanceInches():
    return (FRUIT_HEIGHT_IN / 2) / math.atan(math.tan((FRUIT_HEIGHT_IN / 2) / CALIBRATION_DISTANCE_IN) * vision.largest_object().height / CALIBRATION_HEIGHT_PX)

X_FOV = 61

def findXOffsetDegrees(x: float):
    return (160 - x) / 320 * X_FOV

def printSnapshot(signature: Signature):
    objects = vision.take_snapshot(signature)  
    if objects:
        print("sig: " + getSignatureName(signature), "deg: " + str(findXOffsetDegrees(vision.largest_object().centerX)), "dist: " + str(findSignatureDistanceInches()))  
    else:
        print("No " + getSignatureName(signature))
    wait(20)

prevButtonPressing = False
def buttonPressed():
    global prevButtonPressing
    returnValue = False
    if button.pressing() and not prevButtonPressing:
        returnValue = True
    prevButtonPressing = button.pressing()
    return returnValue

def handleButtonPress():
    global state
    if state == IDLE_STATE:
        state = FOLLOW_STATE
        print("FOLLOW")
    else:
        state = IDLE_STATE
        print("IDLE")

def idle():
    leftDrive.stop()
    rightDrive.stop()
    arm.spin_to_position(0)

def visionHasTarget():
    returnValue = False
    objects = vision.take_snapshot(TARGET_FRUIT)
    if objects and findSignatureDistanceInches() < TARGET_MAX_DISTANCE_IN:
        returnValue = True
    return returnValue

leftTarget = 0
rightTarget = 0

def followTarget():
    global state
    global leftTarget
    global rightTarget

    objects = vision.take_snapshot(TARGET_FRUIT)
    if objects:
        # dimensional analysis to turn m/s into rpm
        rpm = (FOLLOW_SPEED_M_PER_S * 39.3701 * 60) / (WHEEL_DIAMETER_IN * math.pi)

        effort = findXOffsetDegrees(vision.largest_object().centerX) * ROTATE_KP

        leftDrive.spin(FORWARD, (rpm - effort) * GEAR_RATIO)
        rightDrive.spin(FORWARD, (rpm + effort) * GEAR_RATIO)

        if atTargetDistance():
            state = TOUCH_STATE
            leftTarget = leftDrive.position()
            rightTarget = rightDrive.position()
            print("TOUCH")

def findTarget():
    # dimensional analysis to turn robot rad/sec into wheel rpm
    rpm = (FIND_SPEED_RAD_PER_S * WHEEL_BASE_IN * 60) / (2 * math.pi)

    leftDrive.spin(REVERSE, rpm * GEAR_RATIO)
    rightDrive.spin(FORWARD, rpm * GEAR_RATIO)

def atTargetDistance():
    returnValue = False
    objects = vision.take_snapshot(TARGET_FRUIT)
    if objects:
        returnValue = findSignatureDistanceInches() < TARGET_DISTANCE_IN
    return returnValue

def touchFruit():
    leftDrive.spin_to_position(leftTarget)
    rightDrive.spin_to_position(rightTarget)
    rightDrive.stop()
    arm.spin_to_position(ARM_TOUCH_FRUIT_ANGLE_DEG * GEAR_RATIO)

while True:
    if buttonPressed():
        handleButtonPress()

    if state == IDLE_STATE:
        idle()
    elif state == FOLLOW_STATE:
        if visionHasTarget():
            followTarget()
        else:
            findTarget()
    elif state == TOUCH_STATE:
        touchFruit()