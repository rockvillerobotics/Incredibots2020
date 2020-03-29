from wallaby import *
from decorators import *
from objects import *
import constants as c
import movement as m
import utils as u

# -------------------------------States------------------------

def pressed_left():
    return(digital(c.LEFT_LIMIT_SWITCH) == 1)

def unpressed_left():
    return(digital(c.LEFT_LIMIT_SWITCH) == 0)

def pressed_right():
    return(digital(c.RIGHT_LIMIT_SWITCH) == 1)

def unpressed_right():
    return(digital(c.RIGHT_LIMIT_SWITCH) == 0)

def pressed_both():
    return(pressed_left() or pressed_right())

def unpressed_either():
    return(not(pressed_left() or pressed_right()))

# -------------------------------Wait Until Event Commands--------------------

def wait_until(boolean_function, time=c.SAFETY_TIME):
    if time == 0:
        time = c.SAFETY_TIME_NO_STOP
    sec = seconds() + time / 1000.0
    while seconds() < sec and not(boolean_function()):
        msleep(1)

# -------------------------------Basic Align Commands ------------------------

@print_function_name
def align_close():
    # Aligns completely on the side of the line closest to the claw
    left_backwards_until_white()
    right_backwards_until_white()
    right_forwards_until_black()
    left_forwards_until_black()


@print_function_name
def align_far(left_first=True):
    # Aligns completely on the side of the line closest to the camera
    if left_first == True:
        right_forwards_until_white()
        left_forwards_until_white()
        left_backwards_until_black()
        right_backwards_until_black()
    else:
        left_forwards_until_white()
        right_forwards_until_white()
        right_backwards_until_black()
        left_backwards_until_black()


# -------------------------------Single Motor Align Commands ------------------------

@print_function_name_with_arrows
def left_forwards_until(boolean_function, time=c.SAFETY_TIME, should_stop=True):
    # Left motor goes forwards until right tophat senses black
    left_motor.accelerate_to(left_motor.base_power)
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    wait_until(boolean_function, time)
    if should_stop:
        m.deactivate_motors()


@print_function_name_with_arrows
def right_forwards_until(boolean_function, time=c.SAFETY_TIME, should_stop=True):
    # Right motor goes forwards until right tophat senses black
    right_motor.accelerate_to(right_motor.base_power)
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    wait_until(boolean_function, time)
    if should_stop:
        m.deactivate_motors()


@print_function_name_with_arrows
def left_backwards_until(boolean_function, time=c.SAFETY_TIME, should_stop=True):
    # Left motor goes backwards until left tophat senses black
    left_motor.accelerate_to(left_motor.base_power)
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    wait_until(boolean_function, time)
    if should_stop:
        m.deactivate_motors()


@print_function_name_with_arrows
def right_backwards_until(boolean_function, time=c.SAFETY_TIME, should_stop=True):
    # Right motor goes back until right tophat senses black
    right_motor.accelerate_to(right_motor.base_power)
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    wait_until_black_right(time)
    if should_stop:
        m.deactivate_motors()


# -------------------------------Point Turn Align Commands ------------------------

@print_function_name_with_arrows
def turn_left_until(boolean_function, time=c.SAFETY_TIME, should_stop=True):
    m.base_turn_left()
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    wait_until(boolean_function, time)
    if should_stop:
        m.deactivate_motors()


@print_function_name_with_arrows
def turn_right_until(boolean_function, time=c.SAFETY_TIME, should_stop=True):
    m.base_turn_right()
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    wait_until(boolean_function, time)
    if should_stop:
        m.deactivate_motors()


# -------------------------------Driving Align Commands ------------------------

@print_function_name
def snap_to_line_left(turn_time=c.SAFETY_TIME):
    drive_through_line_third()
    turn_left_until_black(turn_time)


@print_function_name
def snap_to_line_right(turn_time=c.SAFETY_TIME):
    drive_through_line_third()
    turn_right_until_black(turn_time)


@print_function_name_with_arrows
def drive_until(boolean_function, time=c.SAFETY_TIME, should_stop=True):
    m.base_drive()
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    wait_until(boolean_function, time)
    if should_stop:
        m.deactivate_motors()


@print_function_name
def drive_through_line_left(time=c.SAFETY_TIME, should_stop=True):
    drive_until(left.senses_black, should_stop=False)
    drive_until(left.senses_white, time, should_stop)


@print_function_name
def drive_through_line_right(time=c.SAFETY_TIME, should_stop=True):
    drive_until(right.senses_black, should_stop=False)
    drive_until(right.senses_white, time, should_stop)


@print_function_name
def drive_through_line_third(time=c.SAFETY_TIME, should_stop=True):
    drive_until(third.senses_black, should_stop=False)
    drive_until(third.senses_white, time, should_stop)


@print_function_name
def drive_through_two_lines_third(time=c.SAFETY_TIME, should_stop=True):  # Drives without stopping the motors in between
    drive_until(third.senses_black, should_stop=False)
    drive_until(third.senses_white, should_stop=False)
    drive_until(third.senses_black, should_stop=False)
    drive_until(third.senses_white, time, should_stop)


@print_function_name_with_arrows
def backwards_until(boolean_function, time=c.SAFETY_TIME, should_stop=True):
    m.base_backwards()
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    wait_until(boolean_function, time)
    if should_stop:
        m.deactivate_motors()


@print_function_name
def backwards_through_line_left(time=c.SAFETY_TIME, should_stop=True):
    backwards_until(left.senses_black, should_stop=False)
    backwards_until(left.white, time, should_stop)


@print_function_name
def backwards_through_line_third(time=c.SAFETY_TIME, should_stop=True):
    backwards_until(third.senses_black, should_stop=False)
    backwards_until(third.senses_white, time, should_stop)


@print_function_name
def backwards_through_line_right(time=c.SAFETY_TIME, should_stop=True):
    backwards_until(right.senses_black, should_stop=False)
    backwards_until(right.senses_white, time, should_stop)


#-----------------------Basic Gyro Commands---------------------------------------------    

def get_change_in_angle():
    return(gyro_z())

#-----------------------Gyro-Based Movement Commands-------------------------------------
# The gyro sensor can determine what angle the robot is at any given point in time. So, if the gyro sensor senses
# an angle other than 0, then it is clear that the bot is veering. So, the robot veers in the opposite direction to
# reduce the error proportionally to how big the error is.

@print_function_name_with_arrows
def drive_gyro(time, should_stop=True):
    angle = 0
    error = 0
    memory = 0
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        left_speed = left_motor.base_power + (error + memory)
        right_speed = right_motor.base_power - (error + memory)
        m.activate_motors(left_speed, right_speed)
        msleep(10)
        angle += (get_change_in_angle() - u.gyro_bias) * 10
        error = 0.034470956 * angle  # Positive error means veering left. Negative means veering right.
        memory += 0.001 * error
    if should_stop:
        m.deactivate_motors()


@print_function_name_with_arrows
def backwards_gyro(time, should_stop=True):
    angle = 0
    error = 0
    memory = 0
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        left_speed = -left_motor.base_power + (error + memory)
        right_speed = -right_motor.base_power - (error + memory)
        m.activate_motors(left_speed, right_speed)
        msleep(10)
        angle += (get_change_in_angle() - u.gyro_bias) * 10
        error = 0.034470956 * angle  # Positive error means veering right. Negative means veering left.
        memory += 0.001 * error
    if should_stop:
        m.deactivate_motors()


#-----------------------Gyro-Based Turning Commands-------------------------------------
# The robot turns until the gyro sensor senses the desired angle.

def turn_gyro(degrees, should_stop=True):
    angle = 0
    target_angle = degrees * c.DEGREE_CONVERSION_RATE
    if target_angle > 0:
        m.base_turn_left()
        sec = seconds() + c.SAFETY_TIME
        while angle < target_angle and seconds() < sec:
            msleep(10)
            angle += (get_change_in_angle() - u.gyro_bias) * 10
    else:
        m.base_turn_right()
        sec = seconds() + c.SAFETY_TIME
        while angle > target_angle and seconds() < sec:
            msleep(10)
            angle += (get_change_in_angle() - u.gyro_bias) * 10
    if should_stop:
        m.deactivate_motors()


def turn_left_gyro(degrees=90, should_stop=True):
    print "Starting turn_left_gyro() for " + str(degrees) + " degrees"
    turn_gyro(degrees, should_stop)


def turn_right_gyro(degrees=90, should_stop=True):
    print "Starting turn_right_gyro() for " + str(degrees) + " degrees"
    turn_gyro(-degrees, should_stop)


#----------------Gyro-Based Movement Until Tophat-----------------
# Basic gyro-based movement until the tophat senses black or white. This ensures that the
# bot doesn't veer on its way to a line.

@print_function_name_with_arrows
def drive_gyro_until(boolean_function, time=c.SAFETY_TIME, should_stop=True):
    angle = 0
    error = 0
    memory = 0
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    sec = seconds() + time / 1000.0
    while seconds() < sec and not(boolean_function()):
        left_speed = left_motor.base_power + (error + memory)
        right_speed = right_motor.base_power - (error + memory)
        m.activate_motors(left_speed, right_speed)
        msleep(10)
        angle += (get_change_in_angle() - u.gyro_bias) * 10
        error = 0.034470956 * angle  # Positive error means veering left. Negative means veering right.
        memory += 0.00001 * error
    if should_stop:
        m.deactivate_motors()


@print_function_name_with_arrows
def backwards_gyro_until(boolean_function, time=c.SAFETY_TIME, should_stop=True):
    angle = 0
    error = 0
    memory = 0
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    sec = seconds() + time / 1000.0
    while seconds() < sec and not(boolean_function()):
        left_speed = -left_motor.base_power + (error + memory)
        right_speed = -right_motor.base_power - (error + memory)
        m.activate_motors(left_speed, right_speed)
        msleep(10)
        angle += (get_change_in_angle() - u.gyro_bias) * 10
        error = 0.034470956 * angle  # Positive error means veering left. Negative means veering right.
        memory += 0.001 * error
    if should_stop:
        m.deactivate_motors()


@print_function_name
def drive_gyro_through_line_left(time=c.SAFETY_TIME, should_stop=True):
    drive_gyro_until(left.senses_black, should_stop=False)
    drive_gyro_until(left.senses_white, time, should_stop)


@print_function_name
def drive_gyro_through_line_right(time=c.SAFETY_TIME, should_stop=True):
    drive_gyro_until(right.senses_black, should_stop=False)
    drive_gyro_until(right.senses_white, time, should_stop)


@print_function_name
def drive_gyro_through_line_third(time=c.SAFETY_TIME, should_stop=True):
    drive_gyro_until(third.senses_black, should_stop=False)
    drive_gyro_until(third.senses_white, time, should_stop)


@print_function_name
def drive_gyro_through_line_fourth(time=c.SAFETY_TIME, should_stop=True):
    drive_gyro_until(fourth.senses_black, should_stop=False)
    drive_gyro_until(fourth.senses_white, time, should_stop)


@print_function_name
def backwards_gyro_through_line_left(time=c.SAFETY_TIME, should_stop=True):
    backwards_gyro_until(left.senses_black, should_stop=False)
    backwards_gyro_until(left.senses_white, time, should_stop)


@print_function_name
def backwards_gyro_through_line_right(time=c.SAFETY_TIME, should_stop=True):
    backwards_gyro_until(right.senses_black, should_stop=False)
    backwards_gyro_until(right.senses_white, time, should_stop)


@print_function_name
def backwards_gyro_through_line_third(time=c.SAFETY_TIME, should_stop=True):
    backwards_gyro_until(third.senses_black, should_stop=False)
    backwards_gyro_until(third.senses_white, time, should_stop)


@print_function_name
def drive_gyro_to_line_left(time=c.SAFETY_TIME, should_stop=True):
    drive_gyro_until(left.senses_white, should_stop=False)
    drive_gyro_until(left.senses_black, (time, should_stop)


@print_function_name
def drive_gyro_to_line_right(time=c.SAFETY_TIME, should_stop=True):
    drive_gyro_until(right.senses_white, should_stop=False)
    drive_gyro_until(right.senses_black, time, should_stop)


@print_function_name
def drive_gyro_to_line_third(time=c.SAFETY_TIME, should_stop=True):
    drive_gyro_until(third.senses_white, should_stop=False)
    drive_gyro_until(third.senses_black, time, should_stop)


@print_function_name
def backwards_gyro_to_line_left(time=c.SAFETY_TIME, should_stop=True):
    backwards_gyro_until(left.senses_white, should_stop=False)
    backwards_gyro_until(left.senses_black, time, should_stop)


@print_function_name
def backwards_gyro_to_line_right(time=c.SAFETY_TIME, should_stop=True):
    backwards_gyro_until(right.senses_white, should_stop=False)
    backwards_gyro_until(right.senses_black, time, should_stop)


@print_function_name
def backwards_gyro_to_line_third(time=c.SAFETY_TIME, should_stop=True):
    backwards_gyro_until(third.senses_white, should_stop=False)
    backwards_gyro_until(third.senses_black, time, should_stop)

#----------------Webcam-----------------

def initialize_camera():
    # Wait two seconds for camera to initialize
    print "Initializing Camera"
    i = 0  # Counter
    print "Starting Step 1..."
    while i < 55:
        camera_update()
        i += 1
        msleep(1)
    print "Finished Step 100\n"

#----------------New Stuff-------------------