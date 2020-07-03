from wombat import *
from decorators import *
from objects import *
import constants as c
import movement as m


 def activate_motors(left_motor_power=c.BASE_VALUE, right_motor_power=c.BASE_VALUE):
    if left_motor_power == c.BASE_VALUE:
        left_motor_power = left_motor.base_power
    if right_motor_power == c.BASE_VALUE:
        right_motor_power = right_motor.base_power
    if abs(left_motor_power - left_motor.current_power) > 600
            or abs(right_motor_power - right_motor.current_power) > 600
            or left_motor.current_power == 0
            or right_motor.current_power == 0:
        left_velocity_change = (left_motor_power - left_motor.current_power) / 30
        right_velocity_change = (right_motor_power - right_motor.current_power) / 30
        while abs(left_motor.current_power - left_motor_power) > 100 and abs(right_motor.current_power - right_motor_power) > 100:
            new_power = left_motor.current_power + left_velocity_change
            left_motor.set_power(new_power)
            new_power = right_motor.current_power + right_velocity_change
            right_motor.set_power(new_power)
            msleep(1)
    left_motor.set_power(left_motor_power)
    right_motor.set_power(right_motor_power)  # Ensures actual desired value is reached.


def deactivate_motors():
    left_motor.set_power(0)
    right_motor.set_power(0)
    left_motor.current_power = 0
    right_motor.current_power = 0   


def base_drive(speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * left_motor.base_power), int(speed_multiplier * right_motor.base_power))


def base_turn_left(speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * -1 * left_motor.base_power), int(speed_multiplier * right_motor.base_power))


def base_turn_right(speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * left_motor.base_power), int(speed_multiplier * -1 * right_motor.base_power))


def base_backwards(speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * -1 * left_motor.base_power), int(speed_multiplier * -1 * right_motor.base_power))

#------------------------------- Movement Commands-------------------------------
# The most basic of movement. Turns on wheels for a certain amount of time, and then turns off the wheels.
# There is a lot of mumbo jumbo here to keep consistency with the rest of the code, but if you can understand this
# you can understand every other command here.

def drive(time=c.DEFAULT_DRIVE_TIME, should_stop=True, speed_multiplier=1.0):
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    base_drive(speed_multiplier)
    print "Drive forwards for %d ms" % time
    msleep(time)
    if should_stop:
        deactivate_motors()


def turn_left(time=c.LEFT_TURN_TIME, should_stop=True, speed_multiplier=1.0):
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    base_turn_left(speed_multiplier)
    print "Turn left for %d ms" % time
    msleep(time)
    if should_stop:
        deactivate_motors()


def turn_right(time=c.RIGHT_TURN_TIME, should_stop=True, speed_multiplier=1.0):
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    base_turn_right(speed_multiplier)
    print "Turn right for %d ms" % time
    msleep(time)
    if should_stop:
        deactivate_motors()


def backwards(time=c.DEFAULT_BACKWARDS_TIME, should_stop=True, speed_multiplier=1.0):
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    base_backwards(speed_multiplier)
    print "Drive backwards for %d ms"%time
    msleep(time)
    if should_stop:
        deactivate_motors()


def stop_for(time=1000):  # Same as msleep command, but stops the wheels.
    deactivate_motors()
    msleep(time)

#------------------------Movement until Event------------------------------
# Legobot moves until an event.

@print_function_name_with_arrows
def drive_until(boolean_function, time=c.SAFETY_TIME, should_stop=True):
    m.base_drive()
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    wait_until(boolean_function, time)
    if should_stop:
        m.deactivate_motors()


@print_function_name_with_arrows
def backwards_until(boolean_function, time=c.SAFETY_TIME, should_stop=True):
    m.base_backwards()
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    wait_until(boolean_function, time)
    if should_stop:
        m.deactivate_motors()


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