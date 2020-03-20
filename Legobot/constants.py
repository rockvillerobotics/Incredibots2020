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
    LEFT_TOPHAT = 1
    RIGHT_TOPHAT = 2
    THIRD_TOPHAT = 3
    FOURTH_TOPHAT = 4

    # Analog Values
    LEFT_TOPHAT_VALUE_MIDPOINT = 721  # If more, black. If less, white.
    RIGHT_TOPHAT_VALUE_MIDPOINT = 785  # If more, black. If less, white.
    THIRD_TOPHAT_VALUE_MIDPOINT = 2083  # If more, black. If less, white.
    FOURTH_TOPHAT_VALUE_MIDPOINT = 2083
    LFOLLOW_REFRESH_RATE = 30  # Default amount of time before tophats check their black/white status again.

    # Digital Sensors
    LEFT_LIMIT_SWITCH = 0
    RIGHT_LIMIT_SWITCH = 1

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
    # -- Clone Motors ---------------

    # Clone Motor Ports
    LEFT_MOTOR = 2
    RIGHT_MOTOR = 3
    AMBULANCE_ARM_MOTOR = 0

    # Clone Base Motor Powers
    BASE_LM_POWER = 900
    BASE_RM_POWER = -900
    HALF_LM_POWER = BASE_LM_POWER / 2
    HALF_RM_POWER = BASE_RM_POWER / 2
    FULL_LM_POWER = BASE_LM_POWER
    FULL_RM_POWER = BASE_RM_POWER
    LFOLLOW_SMOOTH_LM_POWER = int(.7 * BASE_LM_POWER)
    LFOLLOW_SMOOTH_RM_POWER = int(.7 * BASE_RM_POWER)
    OFF = 999999

    # Clone Motor Power Trackers
    CURRENT_LM_POWER = 0
    CURRENT_RM_POWER = 0

    # Clone Motor Timings
    RIGHT_TURN_TIME = 900  # Need to test turn timings periodically. They change as battery charge changes, or on new boards.
    LEFT_TURN_TIME = 900
    DEFAULT_DRIVE_TIME = 500
    DEFAULT_BACKWARDS_TIME = 500

    # -------------------------------Servos------------------------

    # Clone Servo Limits
    MAX_SERVO_POS = 1900  # Cannot physically exceed 2047 or servo will break. Metal servos are more affected.
    MIN_SERVO_POS = 100  # Cannot physically exceed 0 or servo will break. Metal servos are more affected.
    SERVO_DELAY = 500  # Time needed to move a servo (need more testing to find a good value).

    # Clone Arm Servo
    ARM_SERVO = 3
    MAX_ARM_SERVO_POS = MAX_SERVO_POS
    MIN_ARM_SERVO_POS = MIN_SERVO_POS
    ARM_UP_POS = 669
    ARM_DOWN_POS = 1770

    # Clone Claw Servo
    CLAW_SERVO = 1
    MAX_CLAW_SERVO_POS = 1024
    MIN_CLAW_SERVO_POS = 1024
    CLAW_OPEN_POS = 458  # Claw fingers form a 180 degree line
    CLAW_CLOSE_POS = 1024
    CLAW_TRUCK_CLOSE_POS = 1418
    CLAW_LESS_OPEN_POS = 928
    CLAW_CHECKING_POS = 1024

    # Clone Micro Servo
    MICRO_SERVO = 0

    # Clone Starting Positions
    STARTING_ARM_POS = 1024
    STARTING_CLAW_POS = 1024
    STARTING_MICRO_POS = 1024

    # -------------------------------Sensors------------------------

    # Clone Analog Ports
    LIGHT_SENSOR = 0
    LEFT_TOPHAT = 1
    RIGHT_TOPHAT = 2
    THIRD_TOPHAT = 3
    FOURTH_TOPHAT = 4

    # Clone Analog Values
    LEFT_TOPHAT_VALUE_MIDPOINT = 721  # If more, black. If less, white.
    RIGHT_TOPHAT_VALUE_MIDPOINT = 785  # If more, black. If less, white.
    THIRD_TOPHAT_VALUE_MIDPOINT = 2083  # If more, black. If less, white.
    FOURTH_TOPHAT_VALUE_MIDPOINT = 2083
    LFOLLOW_REFRESH_RATE = 30  # Default amount of time before tophats check their black/white status again.

    # Clone Digital Sensors
    RIGHT_BUMP_SENSOR = 0
    BUMP_SENSOR = 1

    # Clone Gyro Values
    DEGREE_CONVERSION_RATE = 6281.8888889

    # Clone Camera Colors
    YELLOW = 0
    RED = 1
    GREEN = 2

    # Clone Camera Zones
    NEAR_ZONE = -1
    FAR_ZONE = 1

    # Clone PID Lfollow Values
    MAX_TOPHAT_VALUE_RIGHT = 3200
    MIN_TOPHAT_VALUE_RIGHT = 128
    MAX_TOPHAT_VALUE_LEFT = 3200
    MIN_TOPHAT_VALUE_LEFT = 128  # These values dont do anything unless calib command doesnt work right.
    MAX_TOPHAT_VALUE_THIRD = 3200
    MIN_TOPHAT_VALUE_THIRD = 128
    KP = 10
    KI = 0.161
    KD = 1
    KP_SAFE = 7
    KI_SAFE = 0.061
    KD_SAFE = 1

    # Clone Miscellaneous Values
    SAFETY_TIME = 15000  # This is the while loop time limit that ensures we don't have an infinite loop.
    SAFETY_TIME_NO_STOP = SAFETY_TIME + 1
    BASE_TIME = 9999
    BASE_VALUE = 99999
    START_TIME = 0
    SECONDS_DELAY = 0
    IS_GRAPHICS_OPEN = False