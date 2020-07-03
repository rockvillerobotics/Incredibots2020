import ctypes
KIPR=ctypes.CDLL("/usr/lib/libkipr.so")
from Motor import Motor
from Servo import Servo
from Tophat import Tophat
from Limit import Limit
import constants as c

#-------------------------------Clone Bot Definitions------------------------
# This is used to determine which robot is which based on how many color channels each bot has.

def MAIN_BOT_CHANNEL_COUNT():
    return(KIPR.get_channel_count() == 3)

def CLONE_BOT_CHANNEL_COUNT():
    return(KIPR.get_channel_count() == 4)  # If the bot has 4 camera channels, then it is the clone bot.

IS_MAIN_BOT = MAIN_BOT_CHANNEL_COUNT()  # Left button for main

IS_CLONE_BOT = CLONE_BOT_CHANNEL_COUNT()  # Right button for clone

if IS_MAIN_BOT:
    #---------------Motor Objects--------------------
    # Parameters: port, base value, direction
    # Direction is the coefficient to motor speed. It can reverse motors. 
    # The first two motor definitions must be the left and right motors.
    
    left_motor = Motor(2, 900, -1)
    right_motor = Motor(3, 900, 1)
    
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
    front_limit = Limit(0)
    

elif IS_CLONE_BOT:
    pass
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
 
 
    
    