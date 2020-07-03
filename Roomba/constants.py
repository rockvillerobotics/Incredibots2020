# This is a meaningless value. It is meant to be a placeholder for old constants
# that aren't currently being used but may be used in the future.
NO_CURRENT_VALUE = 7

#---------------------------------------------Motors-------------------------------------------

# Motor Ports (Not real - made to be consistent with Legobot)
LEFT_MOTOR = 2
RIGHT_MOTOR = 3
ARM_MOTOR = NO_CURRENT_VALUE

# Running Motor Powers
CURRENT_LM_POWER = 0
CURRENT_RM_POWER = 0
#---------------------------------------------Servos-------------------------------------------
    
# Servo Base Positions
ARM_UP_POS = 138
ARM_DOWN_POS = 1387
ARM_JUST_BARELY_ON_T_POS = 654
ARM_DELIVERY_POS = 350
ARM_JUST_BELOW_T_POS = 425 # 350
ARM_HALF_UP_POS = ARM_UP_POS - 815
ARM_TESTING_POS = ARM_UP_POS
ARM_SUPER_HIGH_POS = ARM_UP_POS + 310
# The arm is perpindicular to the ground.
ARM_START_POS = ARM_UP_POS


MAGNET_ARM_UP_POS = 325
MAGNET_ARM_DOWN_POS = 1857
MAGNET_ARM_START_POS = MAGNET_ARM_DOWN_POS
    

CLAW_OPEN_POS = 1024
CLAW_CLOSE_POS = 1024
CLAW_START_POS = CLAW_OPEN_POS


WRIST_OUT_POS = 1000#RANDOM
WRIST_IN_POS = 1054
WRIST_START_POS = WRIST_IN_POS

# Micro Servo Positions
MICRO_UP_POS = 1517
MICRO_RETRACTED_POS = 799
MICRO_START_POS = MICRO_RETRACTED_POS

#---------------------------------------------Movement---------------------------------------------

# Turn Values
RIGHT_TURN_TIME = 891
LEFT_TURN_TIME = 891

# Motor Values
BASE_LM_POWER = 199
BASE_RM_POWER = 211
FULL_LM_POWER = BASE_LM_POWER
FULL_RM_POWER = BASE_RM_POWER
HALF_LM_POWER = int(BASE_LM_POWER) / 2
HALF_RM_POWER = int(BASE_RM_POWER) / 2
BASE_ARM_MOTOR_POWER = 100

# Default Drive Times
DEFAULT_DRIVE_TIME = 500
DEFAULT_BACKWARDS_TIME = 500

#----------------------------------------------Sensors---------------------------------------------

# Analog Sensor Ports
# Cliffs are built into the Roomba, no need for analog ports.
DEPTH_SENSOR = 0
SECOND_DEPTH_SENSOR = 1
CLAW_TOPHAT = 2
LIGHT_SENSOR = 5

# Locations
LEFT = 1
RIGHT = -1

# Line Follow Modes
STANDARD = 1
INSIDE_LINE = -1

# Analog Sensor Values
LCLIFF_BW = 2000  # Min is 0, max is 4950
RCLIFF_BW = 2000  # If more white, if less black
LFCLIFF_BW = 2000
RFCLIFF_BW = 2000
CLAW_TOPHAT_BW = 3000
    
CLAW_TOPHAT_COUPLER_READING = 2500
CLAW_TOPHAT_NOTHING_READING = 300

LFOLLOW_REFRESH_RATE = 10

# Smooth Lfollow Motor Values
LFOLLOW_SMOOTH_LM_POWER = int (.7 * BASE_LM_POWER)
LFOLLOW_SMOOTH_RM_POWER = int (.7 * BASE_RM_POWER)

# Cliff Calibration Values
MIN_SENSOR_VALUE_LCLIFF = 90000
MAX_SENSOR_VALUE_LCLIFF = 0
MAX_SENSOR_VALUE_RCLIFF = 0
MIN_SENSOR_VALUE_RCLIFF = 90000
MAX_SENSOR_VALUE_LFCLIFF = 0
MIN_SENSOR_VALUE_LFCLIFF = 90000
MAX_SENSOR_VALUE_RFCLIFF = 0
MIN_SENSOR_VALUE_RFCLIFF = 90000

# PID Line Follow Values
KP = 2.222
KI = 0.0357
KD = 0.222

# Depth Sensor Values
DEPTH_CF = 1320
SECOND_DEPTH_CF = 720

# Gyro Sensor Values
AVG_BIAS = 0
DEGREE_CONVERSION_RATE = 5950  # 6236.7777777777778
ROBOT_ANGLE = 0
GYRO_TIME = 10

# Digital Sensors
LIMIT_SWITCH = NO_CURRENT_VALUE
BUMP_SWITCH = 0

# Digital Variables
FIRST_BUMP = True

# Misc Values - Placeholder variables that imply the usage of another value
BASE_POWER = 99999
BASE_TIME = 999999999
SAFETY_TIME = 15000
SAFETY_TIME_NO_STOP = SAFETY_TIME + 1
HIGHER = 420