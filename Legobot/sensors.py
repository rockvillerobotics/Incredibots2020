from wallaby import *
from decorators import *
from objects import *
import constants as c
import gyro as g
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
    drive_until(left.black, should_stop=False)
    drive_until(white.left, time, should_stop)


@print_function_name
def drive_through_line_right(time=c.SAFETY_TIME, should_stop=True):
    drive_until(right.black, should_stop=False)
    drive_until(right.white, time, should_stop)


@print_function_name
def drive_through_line_third(time=c.SAFETY_TIME, should_stop=True):
    drive_until(third.black, should_stop=False)
    drive_until(third.white, time, should_stop)


@print_function_name
def drive_through_two_lines_third(time=c.SAFETY_TIME, should_stop=True):  # Drives without stopping the motors in between
    drive_until(third.black, should_stop=False)
    drive_until(third.white, should_stop=False)
    drive_until(third.black, should_stop=False)
    drive_until(third.white, time, should_stop)


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
    backwards_until(left.black, should_stop=False)
    backwards_until(left.white, time, should_stop)


@print_function_name
def backwards_through_line_third(time=c.SAFETY_TIME, should_stop=True):
    backwards_until(third.black, should_stop=False)
    backwards_until(third.white, time, should_stop)


@print_function_name
def backwards_through_line_right(time=c.SAFETY_TIME, should_stop=True):
    backwards_until(right.black, should_stop=False)
    backwards_until(right.white, time, should_stop)
