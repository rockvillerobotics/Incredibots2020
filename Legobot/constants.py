"""
When possible, make values into constants so they can be easily changed throughout the code at once.
Constants are subject to change, so make sure to check the values to be certain that they are right.
Note: All constant timings are assumed to be in milliseconds unless otherwise specified.
"""

import ctypes
KIPR=ctypes.CDLL("/usr/lib/libkipr.so")

#-------------------------------Motors, Servos, and Sensors------------------------

# Locations/Directions
LEFT = 1
RIGHT = -1
FRONT = 1
BACK = -1
TOP = 1
BOTTOM = -1

# Motor Timings
RIGHT_TURN_TIME = 900  # Need to test turn timings periodically. They change as battery charge changes, or on new boards.
LEFT_TURN_TIME = 900
DEFAULT_DRIVE_TIME = 500
DEFAULT_BACKWARDS_TIME = 500

#-------------------------------Sensors------------------------

# Analog Ports
LIGHT_SENSOR = 0

# Tophat Types
BIG_TOPHAT = 0
SMALL_TOPHAT = 1

# Line Follow Types
STANDARD = 0
INSIDE_LINE = 1

# Gryo Values
DEGREE_CONVERSION_RATE = 6281.8888889

# Camera Colors
YELLOW = 0
RED = 1
GREEN = 2

# Camera Zones
FIRST_ZONE = -1
SECOND_ZONE = 1

# PID Lfollow Values
KP = 10
KI = 0.161
KD = 1
KP_SAFE = 7
KI_SAFE = 0.061
KD_SAFE = 1

# Webcam Values
MAX_LENGTH = 480
MAX_HEIGHT = 260
LEFT_EDGE = 0
RIGHT_EDGE = MAX_LENGTH
TOP_EDGE = 0
BOTTOM_EDGE = MAX_HEIGHT

# Miscellaneous Values
SAFETY_TIME = 15000  # This is the while loop time limit that ensures we don't have an infinite loop.
SAFETY_TIME_NO_STOP = SAFETY_TIME + 1
BASE_TIME = 9999
BASE_VALUE = 99999
START_TIME = 0
SECONDS_DELAY = 0
IS_GRAPHICS_OPEN = False
