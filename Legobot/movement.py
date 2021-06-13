"""Codes involving general motor or servo motion go here"""
import time as seconds
import ctypes
KIPR=ctypes.CDLL("/usr/lib/libkipr.so")
from objects import *
from decorators import *
import constants as c
import sensors as s
import utils as u

#------------------------------- Movement Commands-------------------------------

@print_function_name_with_arrows
def drive_until(boolean_function, *, time=c.SAFETY_TIME, use_gyro=False, should_stop=True):
    """This function goes forwards until an event.

    Args:
        boolean_function (function): The event you go back for until reached.
        time (number, optional): The code will automatically after this amount of time. This is to avoid infinite loops. Defaults to c.SAFETY_TIME.
        use_gyro (bool, optional): The robot will use an internal gyro to straighten its driving. Defaults to False.
        should_stop (bool, optional): The robot will stop after this code ends if this is true. Defaults to True.
    """
    if(use_gyro):
        gyro.drive_gyro_until(boolean_function, time=time, should_stop=should_stop)
    else:    
        base_drive()
        if time == 0:
            should_stop = False
            time = c.SAFETY_TIME
        u.wait_until(boolean_function, time)
        if should_stop:
            deactivate_motors()


@print_function_name_with_arrows
def backwards_until(boolean_function, *, time=c.SAFETY_TIME, use_gyro=False, should_stop=True):
    """This function goes backwards until an event.

    Args:
        boolean_function (function): The event you go back for until reached.
        time (number, optional): The code will automatically after this amount of time. This is to avoid infinite loops. Defaults to c.SAFETY_TIME.
        use_gyro (bool, optional): The robot will use an internal gyro to straighten its driving. Defaults to False.
        should_stop (bool, optional): The robot will stop after this code ends if this is true. Defaults to True.
    """
    if(use_gyro):
        gyro.backwards_gyro_until(boolean_function, time=time, should_stop=should_stop)
    else:    
        base_backwards()
        if time == 0:
            should_stop = False
            time = c.SAFETY_TIME
        u.wait_until(boolean_function, time)
        if should_stop:
            deactivate_motors()


@print_function_name_with_arrows
def turn_left_until(boolean_function, *, time=c.SAFETY_TIME, degrees=0, should_stop=True):
    if(degrees != 0):
        stop_or_not = should_stop
        gyro.turn_left_gyro(degrees, should_stop=stop_or_not)
    else:    
        base_turn_left()
        if time == 0:
            should_stop = False
            time = c.SAFETY_TIME
        u.wait_until(boolean_function, time)
        if should_stop:
            deactivate_motors()


@print_function_name_with_arrows
def turn_right_until(boolean_function, *, time=c.SAFETY_TIME, degrees=0, should_stop=True):
    if(degrees != 0):
        stop_or_not = should_stop
        gyro.turn_right_gyro(degrees, should_stop=stop_or_not)
    else:
        base_turn_right()
        if time == 0:
            should_stop = False
            time = c.SAFETY_TIME
        u.wait_until(boolean_function, time)
        if should_stop:
            deactivate_motors()
            
#------------------------------- Base Commands -------------------------------
#  These commands start the motors in a certain way. They are just activate motors but in a specific direction.

def base_drive(speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * left_motor.base_power), int(speed_multiplier * right_motor.base_power))


def base_turn_left(speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * -1 * left_motor.base_power), int(speed_multiplier * right_motor.base_power))


def base_turn_right(speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * left_motor.base_power), int(speed_multiplier * -1 * right_motor.base_power))


def base_backwards(speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * -1 * left_motor.base_power), int(speed_multiplier * -1 * right_motor.base_power))

#------------------------------- Timed Movement Commands-------------------------------

# Shorthand for moving until time. Should stop is passed to the parent function.
def drive(time, should_stop=True):
    drive_until(u.always_false, time=time, should_stop=should_stop)


def backwards(time, should_stop=True):
    backwards_until(u.always_false, time=time, should_stop=should_stop)


# By default the turns will be 90 degree turns. The exact time value needs calibration.
def turn_left(time=c.LEFT_TURN_TIME, should_stop=True):
    turn_left_until(u.always_false, time=time, should_stop=should_stop)


def turn_right(time=c.RIGHT_TURN_TIME, should_stop=True):
    turn_right_until(u.always_false, time=time, should_stop=should_stop)

#------------------------------- Basic Movement Commands -------------------------------
# These commands are really the building blocks of the whole code. They're practical; they're
# built to be used on a daily basis. If you're going to copy something of our code, I would suggest that it be this
# because these are better versions of the wallaby "mav".

def activate_motors(left_motor_power=c.BASE_VALUE, right_motor_power=c.BASE_VALUE):
    if left_motor_power == c.BASE_VALUE:
        left_motor_power = left_motor.base_power
    if right_motor_power == c.BASE_VALUE:
        right_motor_power = right_motor.base_power
    if (abs(left_motor_power - left_motor.current_power) > 600
            or abs(right_motor_power - right_motor.current_power) > 600
            or left_motor.current_power == 0
            or right_motor.current_power == 0):
        left_velocity_change = (left_motor_power - left_motor.current_power) / 30
        right_velocity_change = (right_motor_power - right_motor.current_power) / 30
        while abs(left_motor.current_power - left_motor_power) > 100 and abs(right_motor.current_power - right_motor_power) > 100:
            new_power = left_motor.current_power + left_velocity_change
            left_motor.set_power(new_power)
            new_power = right_motor.current_power + right_velocity_change
            right_motor.set_power(new_power)
            KIPR.msleep(1)
    left_motor.set_power(left_motor_power)
    right_motor.set_power(right_motor_power)  # Ensures actual desired value is reached.


def deactivate_motors():
    left_motor.set_power(0)
    right_motor.set_power(0)
    left_motor.current_power = 0
    right_motor.current_power = 0


#------------------------------- Line Shorthand ---------------------------------------
# These commands are more intuitive ways to move around lines.

@print_function_name
def drive_through_line(tophat, *, time=c.SAFETY_TIME, should_stop=True):
    drive_until(tophat.senses_black, should_stop=False)
    drive_until(tophat.senses_white, time, should_stop)
    

@print_function_name
def backwards_through_line(tophat, *, time=c.SAFETY_TIME, should_stop=True):
    backwards_until(tophat.senses_black, should_stop=False)
    backwards_until(tophat.senses_white, time, should_stop)


#------------------------------- Tics Movement Commands -------------------------------
# Basic movment for a certain distance, measured in wallaby "tics." Your guess is as good as mine as to what a
# "tic" is, but it's the universal wallaby unit of distance. Normally there are about 200 tics to an inch.

@print_function_name_with_arrows
def drive_tics(tics, speed_multiplier=1.0, should_stop=True):
    left_motor.clear_tics()
    right_motor.clear_tics()
    base_drive(speed_multiplier)
    while gmpc(c.LEFT_MOTOR) < tics and gmpc(c.RIGHT_MOTOR) > -1 * tics:
        msleep(1)
    if should_stop:
        deactivate_motors()


@print_function_name_with_arrows
def backwards_tics(tics, speed_multiplier=1.0, should_stop=True):
    left_motor.clear_tics()
    right_motor.clear_tics()
    base_backwards(speed_multiplier)
    while gmpc(c.LEFT_MOTOR) > -1 * tics and gmpc(c.RIGHT_MOTOR) < tics:
        msleep(1)
    if should_stop:
        deactivate_motors()


#------------------------------- Servos -------------------------------
# All these commands move the servo to a specified location at a specified speed.
# The more tics per second, the faster the servo moves.

def open_claw(tics=3, ms=1, servo_position=1024):
    print("Open claw to desired position: %d" % servo_position)
    claw_servo.move(servo_pos, tics, ms)  # Checking for faulty values must go before setting position.
    print("Claw opened to position: %d" % get_servo_position(c.CLAW_SERVO))


def close_claw(tics=3, ms=1, servo_pos=1024):
    print("Close claw to desired position: %d" % servo_position)
    claw_servo.move(servo_pos, tics, ms)
    print("Claw closed to position: %d" % get_servo_position(c.CLAW_SERVO))


def lift_arm(tics=3, ms=1, servo_pos=1024):
    print("Set arm servo to desired up position: %d" % servo_position)
    arm_servo.move(servo_pos, tics, ms)
    print("Arm reached up position: %d" % get_servo_position(c.ARM_SERVO))


def lower_arm(tics=3, ms=1, servo_pos=c.BASE_TIME):
    print("Set arm servo to desired down position: %d" % servo_position)
    if servo_position == c.BASE_TIME:
        servo_position = 1024
    arm_servo.move(servo_pos, tics, ms)
    print("Arm reached down position: %d" % get_servo_position(c.ARM_SERVO))
