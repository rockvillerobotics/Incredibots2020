from Legobot.All_Classes.Gyro_Class import Gyro
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
    # Ex: motor_name = Motor(port, base_power, direction)
    # Parameters: port, base_power, direction
    #   Direction is the coefficient to motor speed. It can reverse motors. 
    #   The first two motor definitions must be the left and right motors.
    
    left_motor = Motor(2, 900, -1)
    right_motor = Motor(3, 900, 1)
    
    #---------------Servo Objects-------------------
    # Ex: servo_name = Servo(port, starting_value)
    # Parameters: port, starting_value

    arm_servo = Servo(3, 1024)
    claw_servo = Servo(1, 1024)

    #---------------Tophat Objects------------------
    # Ex: tophat_name = Tophat(port, location=(c.LOCATION, c.LOCATION), tophat_type=c.TYPE)
    # Parameters: port, location, tophat_type
    #   Locations are LEFT, RIGHT, FRONT, and BACK. These help make lfollows
    #   work the way you want. Tophat_types are BIG_TOPHAT and SMALL_TOPHAT

    left = Tophat(1, location=(c.LEFT, c.FRONT), tophat_type=c.BIG_TOPHAT)
    right = Tophat(2, location=(c.RIGHT, c.FRONT), tophat_type=c.BIG_TOPHAT)
    third = Tophat(3, location=(c.LEFT, c.BACK), tophat_type=c.SMALL_TOPHAT)

    #---------------Gyro Objects------------------
    # Ex: gyro_name = Gyro(get_angle_function=gyro_z)
    # Parameters: get_angle_function
    #   As of 2021, the get_angle_function's are: gyro_z, gyro_x, and gyro_y.
    
    gyro = Gyro(gyro_z) 
    
    #---------------Depth Objects--------------------
    # Ex: depth_name = Depth(port, value_midpoint)
    # Parameters: port, value midpoint
    

    #---------------Limit Switch Objects-------------
    # Ex: limit_name = Limit(port)
    # Parameters: port
    front_limit = Limit(0)
    

elif IS_CLONE_BOT:
    #---------------Motor Objects--------------------
    # Ex: motor_name = Motor(port, base_power, direction)
    # Parameters: port, base_power, direction
    #   Direction is the coefficient to motor speed. It can reverse motors. 
    #   The first two motor definitions must be the left and right motors.
    
 
    
    #---------------Servo Objects-------------------
    # Ex: servo_name = Servo(port, starting_value)
    # Parameters: port, starting_value


    
    #---------------Tophat Objects------------------
    # Ex: tophat_name = Tophat(port, location=(c.LOCATION, c.LOCATION), tophat_type=c.TYPE)
    # Parameters: port, location, tophat_type
    #   Locations are LEFT, RIGHT, FRONT, and BACK. These help make lfollows
    #   work the way you want. Tophat_types are BIG_TOPHAT and SMALL_TOPHAT



    #---------------Gyro Objects------------------
    # Ex: gyro_name = Gyro(get_angle_function=gyro_z)
    # Parameters: get_angle_function
    #   As of 2021, the get_angle_function's are: gyro_z, gyro_x, and gyro_y.
    
    gyro = Gyro(gyro_z) 

    #---------------Depth Objects--------------------
    # Ex: depth_name = Depth(port, value_midpoint)
    # Parameters: port, value midpoint
    

    #---------------Limit Switch Objects-------------
    # Ex: limit_name = Limit(port)
    # Parameters: port
 
 
    
    