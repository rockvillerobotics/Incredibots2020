#   When possible, make values into constants so they can be easily changed throughout the code at once.
#   Constants are subject to change, so make sure to check the values to be certain that they are right.
#   Note: All constant timings are assumed to be in milliseconds unless otherwise specified.

from wallaby import *

#-------------------------------Clone Bot Definitions------------------------
# This is used to determine which robot is which based on how many color channels each bot has.

def MAIN_BOT_CHANNEL_COUNT():
    return(get_channel_count() == 3)

def CLONE_BOT_CHANNEL_COUNT():
    return(get_channel_count() == 4)  # If the bot has 4 camera channels, then it is the clone bot.

IS_MAIN_BOT = right_button() == 0 and MAIN_BOT_CHANNEL_COUNT() or left_button() == 1  # Left button for main

IS_CLONE_BOT = left_button() == 0 and CLONE_BOT_CHANNEL_COUNT() or right_button() == 1  # Right button for clone

#-------------------------------Motors, Servos, and Sensors------------------------

if IS_MAIN_BOT:
    
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

    # Analog Values
    LEFT_TOPHAT_VALUE_MIDPOINT = 721  # If more, black. If less, white.
    RIGHT_TOPHAT_VALUE_MIDPOINT = 785  # If more, black. If less, white.
    THIRD_TOPHAT_VALUE_MIDPOINT = 2083  # If more, black. If less, white.
    FOURTH_TOPHAT_VALUE_MIDPOINT = 2083
    LFOLLOW_REFRESH_RATE = 30  # Default amount of time before tophats check their black/white status again.

    # Digital Sensors
    LEFT_LIMIT_SWITCH = 0
    RIGHT_LIMIT_SWITCH = 1

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

else:  # Clone Bot ----------------------------------------------------------------------------------------------------------------
    
    # Clone Locations/Directions
    LEFT = 1
    RIGHT = -1
    FRONT = 1
    BACK = -1
    TOP = 1
    BOTTOM = -1
    
    # Clone Motor Timings
    RIGHT_TURN_TIME = 900  # Need to test turn timings periodically. They change as battery charge changes, or on new boards.
    LEFT_TURN_TIME = 900
    DEFAULT_DRIVE_TIME = 500
    DEFAULT_BACKWARDS_TIME = 500

    #-------------------------------Sensors------------------------

    # Clone Analog Ports
    LIGHT_SENSOR = 0

    # Clone Analog Values
    LEFT_TOPHAT_VALUE_MIDPOINT = 721  # If more, black. If less, white.
    RIGHT_TOPHAT_VALUE_MIDPOINT = 785  # If more, black. If less, white.
    THIRD_TOPHAT_VALUE_MIDPOINT = 2083  # If more, black. If less, white.
    FOURTH_TOPHAT_VALUE_MIDPOINT = 2083
    LFOLLOW_REFRESH_RATE = 30  # Default amount of time before tophats check their black/white status again.

    # Clone Digital Sensors
    LEFT_LIMIT_SWITCH = 0
    RIGHT_LIMIT_SWITCH = 1

    # Clone Gryo Values
    DEGREE_CONVERSION_RATE = 6281.8888889

    # Tophat Types
    BIG_TOPHAT = 0
    SMALL_TOPHAT = 1
    
    # Line Follow Types
    STANDARD = 0
    INSIDE_LINE = 1
    
    # Clone Camera Colors
    YELLOW = 0
    RED = 1
    GREEN = 2

    # Clone Camera Zones
    FIRST_ZONE = -1
    SECOND_ZONE = 1

    # Clone PID Lfollow Values
    KP = 10
    KI = 0.161
    KD = 1
    KP_SAFE = 7
    KI_SAFE = 0.061
    KD_SAFE = 1
    
    # Clone Webcam Values
    MAX_LENGTH = 480
    MAX_HEIGHT = 260
    LEFT_EDGE = 0
    RIGHT_EDGE = MAX_LENGTH
    TOP_EDGE = 0
    BOTTOM_EDGE = MAX_HEIGHT

    # Clone Miscellaneous Values
    SAFETY_TIME = 15000  # This is the while loop time limit that ensures we don't have an infinite loop.
    SAFETY_TIME_NO_STOP = SAFETY_TIME + 1
    BASE_TIME = 9999
    BASE_VALUE = 99999
    START_TIME = 0
    SECONDS_DELAY = 0
    IS_GRAPHICS_OPEN = False