import Motor
import Servo
import Tophat
import constants as c

if IS_MAIN_BOT:
    #---------------Motor Objects--------------------
    # Parameters: port, base value, direction
    # Direction is the coefficient to motor speed. It can reverse motors.

    left_motor = Motor(2, 900, 1)
    right_motor = Motor(3, 900, -1)

    #---------------Servo Objects-------------------
    # Parameters: port, starting_value

    arm_servo = Servo(3, 1024)
    claw_servo = Servo(1, 1024)

    #---------------Tophat Objects------------------
    # Parameters: port, location, tophat_type
    # Locations are left, right, front, and back. These help make lfollows
    #   work the way you want.

    left = Tophat(1, location=(c.LEFT, c.FRONT), tophat_type=c.BIG_TOPHAT)
    right = Tophat(2, location=(c.RIGHT, c.FRONT), tophat_type=c.BIG_TOPHAT)
    third = Tophat(3, location=(c.LEFT, c.BACK), tophat_type=c.SMALL_TOPHAT)

    #---------------Depth Objects--------------------
    # Parameters: port, value midpoint


    #---------------Limit Switch Objects-------------
    # Parameters: port
    
    

elif IS_CLONE_BOT:
    #---------------Motor Objects--------------------
    # Parameters: port, base value, direction
    # Direction is the coefficient to motor speed. It can reverse motors.
    
    
    #---------------Servo Objects-------------------
    # Parameters: port, starting_value
    
    
    #---------------Tophat Objects------------------
    # Parameters: port, location, tophat_type
    # Locations are left, right, front, and back. These help make lfollows
    #   work the way you want.
    
    
    #---------------Depth Objects--------------------
    # Parameters: port, value midpoint


    #---------------Limit Switch Objects-------------
    # Parameters: port
    
    
#-------------------------------Clone Bot Definitions------------------------
# This is used to determine which robot is which based on how many color channels each bot has.

def MAIN_BOT_CHANNEL_COUNT():
    return(get_channel_count() == 3)

def CLONE_BOT_CHANNEL_COUNT():
    return(get_channel_count() == 4)  # If the bot has 4 camera channels, then it is the clone bot.

IS_MAIN_BOT = right_button() == 0 and MAIN_BOT_CHANNEL_COUNT() or left_button() == 1  # Left button for main

IS_CLONE_BOT = left_button() == 0 and CLONE_BOT_CHANNEL_COUNT() or right_button() == 1  # Right button for clone