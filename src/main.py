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
from math import pi

# Brain should be defined by default
brain = Brain()

SIGNATURE_SELECTIVITY = 2.5

# Define vision signatures
LIME = Signature (1, -5461, -4635, -5048, -3641, -3071, -3356, SIGNATURE_SELECTIVITY, 0)
LEMON = Signature (2, -49, 151, 51, -3407, -2521, -2964, SIGNATURE_SELECTIVITY, 0)
TANGERINE = Signature (3, 1121, 3095, 2108, -2765, -2405, -2585, SIGNATURE_SELECTIVITY, 0)
GRAPEFRUIT = Signature (4, 2469, 4465, 3467, 1111, 1439, 1275, SIGNATURE_SELECTIVITY, 0)

vision = Vision(Ports.PORT20, 50, LIME, LEMON, TANGERINE, GRAPEFRUIT)
leftMotor = Motor(Ports.PORT10)
rightMotor = Motor(Ports.PORT1, True)
armMotor = Motor(Ports.PORT7)
imu = Inertial(Ports.PORT3)
button = Bumper(brain.three_wire_port.e)

imu.calibrate()
while imu.is_calibrating():
    pass

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


GEAR_RATIO = 60.0/12.0

def distanceToTurns(distance):
    return distance * GEAR_RATIO / (4 * pi)

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

state = 0
targetHeading = 0
targetDistance = 0

def idleState():
    global state
    leftMotor.stop()
    rightMotor.stop()
    armMotor.stop()
    if button.pressing():
        wait(500)
        state = 1
        

def snapshotState():
    global targetHeading
    global state
    objects = vision.take_snapshot(LIME)
    leftMotor.spin(FORWARD, 30, RPM)
    rightMotor.spin(REVERSE, 30, RPM)
    if (objects):
        xoffset = findXOffsetDegrees(vision.largest_object().centerX)
        if imu.heading() + xoffset >= 360:
            targetHeading = (imu.heading() + xoffset) - 360
        else:
            targetHeading = (imu.heading() + xoffset)
        leftMotor.stop()
        rightMotor.stop()
        state = 2

def centeringState():
    global targetHeading
    global state
    KP = 3
    error = (targetHeading - imu.heading())
    if abs(error) < 0.5:
        leftMotor.stop()
        rightMotor.stop()
        state = 3
    else:
        if error > 180:
            error -= 360
        elif error < -180:
            error += 360
        effort = error * KP
        print(effort)
        leftMotor.spin(FORWARD, effort, RPM)
        rightMotor.spin(REVERSE, effort, RPM)

def drivingState():
    global targetDistance
    global state
    leftMotor.spin_for(FORWARD, distanceToTurns(targetDistance), TURNS, 5, RPM, False)
    rightMotor.spin_for(FORWARD, distanceToTurns(targetDistance), TURNS, 5, RPM, True)
    state = 4

def armState():
    global state
    armMotor.spin_for(FORWARD, 45 * GEAR_RATIO, DEGREES, 5, RPM)

while True:
    if state == 0:
        idleState()
    if state == 1:
        snapshotState()
    if state == 2:
        print(targetHeading)
        print(imu.heading())
        centeringState()
    if state == 3:
        drivingState()
    if state == 4:
        armState()