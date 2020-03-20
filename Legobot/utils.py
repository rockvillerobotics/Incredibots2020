from wallaby import *
import constants as c
import actions as a
import gyro as g
import sensors as s
import movement as m
import Servo
import Motor

#-------------------------------States------------------------

def isLeftPressed():
    return(left_button() == 1)

def isLeftNotPressed():
    return(left_button() == 0)

def isRightPressed():
    return(right_button() == 1)

def isRightNotPressed():
    return(right_button() == 0)

def isBumpSwitchBumped():
    return(digital(c.BUMP_SENSOR) == 1)

def isBumpSwitchNotBumped():
    return(digital(c.BUMP_SENSOR) == 0)

#-------------------------------Commands ------------------------

def wait_for_button():
    print "Press Right Button..."
    while isRightNotPressed():
        msleep(1)
    print "Right button pressed\n"
    msleep(500)


def setup():
# Enables servos and sets them to predefined starting positions. This goes before every run
    print "Starting setup()"
    if c.IS_MAIN_BOT:
        print "I am the main bot"
    elif c.IS_CLONE_BOT:
        print "I am the clone bot"
    else:
        print "Error in bot determination"
        sd()
    graphics_close()
    for motor in Motor.all_motors:
        cmpc(motor)
    for servo in Servo.all_servos:
        enable_servo(servo)
    console_clear()
    print "Setup complete\n\n"


def calibrate_regionals():
    g.calibrate_gyro()
    calibrate_tophats_and_motors()
    print "c.BASE_LM_POWER: " + str(c.BASE_LM_POWER)
    print "c.BASE_RM_POWER: " + str(c.BASE_RM_POWER)
    print "max_sensor_value_left: " + str(max_sensor_value_left)
    print "min_sensor_value_left: " + str(min_sensor_value_left)
    print "LEFT_TOPHAT_BW: " + str(c.LEFT_TOPHAT_BW)
    print "max_sensor_value_right: " + str(max_sensor_value_right)
    print "min_sensor_value_right: " + str(min_sensor_value_right)
    print "RIGHT_TOPHAT_BW: " + str(c.RIGHT_TOPHAT_BW)
    print "max_sensor_value_third: " + str(max_sensor_value_third)
    print "min_sensor_value_third: " + str(min_sensor_value_third)
    print "THIRD_TOPHAT_BW: " + str(c.THIRD_TOPHAT_BW)
    print "max_sensor_value_fourth: " + str(max_sensor_value_fourth)
    print "min_sensor_value_fourth: " + str(min_sensor_value_fourth)
    print "FOURTH_TOPHAT_BW: " + str(c.FOURTH_TOPHAT_BW)


def calibrate_tophats():
    # Code to calibrate the bw values. This goes before every run. Ends with light sensor calibration.
    max_sensor_value_right = 0
    min_sensor_value_right = 90000
    max_sensor_value_left = 0
    min_sensor_value_left = 90000
    max_sensor_value_third = 0
    min_sensor_value_third = 90000
    max_sensor_value_fourth = 0
    min_sensor_value_fourth = 90000
    cmpc(c.LEFT_MOTOR)
    cmpc(c.RIGHT_MOTOR)
    calibrate_tics = 2100
    print "Running calibrate()"
    m.activate_motors(int(-c.BASE_LM_POWER / 2), int(-c.BASE_RM_POWER / 2))
    while abs(gmpc(c.LEFT_MOTOR) - gmpc(c.RIGHT_MOTOR)) / 2  < calibrate_tics:
        if analog(c.RIGHT_TOPHAT) > max_sensor_value_right:
            max_sensor_value_right = analog(c.RIGHT_TOPHAT)
        if analog(c.RIGHT_TOPHAT) < min_sensor_value_right:
            min_sensor_value_right = analog(c.RIGHT_TOPHAT)
        if analog(c.LEFT_TOPHAT) > max_sensor_value_left:
            max_sensor_value_left = analog(c.LEFT_TOPHAT)
        if analog(c.LEFT_TOPHAT) < min_sensor_value_left:
            min_sensor_value_left = analog(c.LEFT_TOPHAT)
        if analog(c.THIRD_TOPHAT) > max_sensor_value_third:
            max_sensor_value_third = analog(c.THIRD_TOPHAT)
        if analog(c.THIRD_TOPHAT) < min_sensor_value_third:
            min_sensor_value_third = analog(c.THIRD_TOPHAT)
        if analog(c.FOURTH_TOPHAT) > max_sensor_value_fourth:
            max_sensor_value_fourth = analog(c.FOURTH_TOPHAT)
        if analog(c.FOURTH_TOPHAT) < min_sensor_value_fourth:
            min_sensor_value_fourth = analog(c.FOURTH_TOPHAT)
        msleep(1)
    m.deactivate_motors()
    # If sensing black when it should be sensing white, increase bias
    # If sensing white when it should be sensing black, decrease bias
    c.LEFT_TOPHAT_BW = int(((max_sensor_value_left + min_sensor_value_left) / 2)) + big_tophat_bias
    c.RIGHT_TOPHAT_BW = int(((max_sensor_value_right + min_sensor_value_right) / 2)) + big_tophat_bias
    c.THIRD_TOPHAT_BW = int(((max_sensor_value_third + min_sensor_value_third) / 2)) + small_tophat_bias
    c.FOURTH_TOPHAT_BW = int(((max_sensor_value_fourth + min_sensor_value_fourth) / 2)) + small_tophat_bias
    c.MAX_TOPHAT_VALUE_RIGHT = max_sensor_value_right
    c.MIN_TOPHAT_VALUE_RIGHT = min_sensor_value_right
    c.MAX_TOPHAT_VALUE_LEFT = max_sensor_value_left
    c.MIN_TOPHAT_VALUE_LEFT = min_sensor_value_left
    c.MAX_TOPHAT_VALUE_THIRD = max_sensor_value_third
    c.MIN_TOPHAT_VALUE_THIRD = min_sensor_value_third
    print "Finished Calibrating. Moving back into starting box...\n"
    # Put commands here to get robot to desired starting position.


def calibrate_tophats_and_motors(big_tophat_bias=-1000, small_tophat_bias=600):
# Code to calibrate the bw values. This goes before every run. Ends with light sensor calibration.
    max_sensor_value_right = 0
    min_sensor_value_right = 90000
    max_sensor_value_left = 0
    min_sensor_value_left = 90000
    max_sensor_value_third = 0
    min_sensor_value_third = 90000
    max_sensor_value_fourth = 0
    min_sensor_value_fourth = 90000
    cmpc(c.LEFT_MOTOR)
    cmpc(c.RIGHT_MOTOR)
    if c.IS_MAIN_BOT:
        calibrate_tics = 2100
    else: # Clone bot
        calibrate_tics = 3000
    print "Running calibrate()"
    angle = 0
    error = 0
    i = 0
    total_left_speed = 0
    total_right_speed = 0
    m.activate_motors(int(-c.BASE_LM_POWER / 2), int(-c.BASE_RM_POWER / 2))
    while abs(gmpc(c.LEFT_MOTOR) - gmpc(c.RIGHT_MOTOR)) / 2  < calibrate_tics:
        left_speed = (-c.BASE_LM_POWER + error) / 2
        right_speed = (-c.BASE_RM_POWER + error) / 2
        total_left_speed += left_speed
        total_right_speed += right_speed
        i += 1
        m.activate_motors(left_speed, right_speed)
        msleep(10)
        angle += (g.get_change_in_angle() - g.bias) * 10
        error = 0.034470956 * angle  # Positive error means veering left. Negative means veering right.
        if analog(c.RIGHT_TOPHAT) > max_sensor_value_right:
            max_sensor_value_right = analog(c.RIGHT_TOPHAT)
        if analog(c.RIGHT_TOPHAT) < min_sensor_value_right:
            min_sensor_value_right = analog(c.RIGHT_TOPHAT)
        if analog(c.LEFT_TOPHAT) > max_sensor_value_left:
            max_sensor_value_left = analog(c.LEFT_TOPHAT)
        if analog(c.LEFT_TOPHAT) < min_sensor_value_left:
            min_sensor_value_left = analog(c.LEFT_TOPHAT)
        if analog(c.THIRD_TOPHAT) > max_sensor_value_third:
            max_sensor_value_third = analog(c.THIRD_TOPHAT)
        if analog(c.THIRD_TOPHAT) < min_sensor_value_third:
            min_sensor_value_third = analog(c.THIRD_TOPHAT)
        if analog(c.FOURTH_TOPHAT) > max_sensor_value_fourth:
            max_sensor_value_fourth = analog(c.FOURTH_TOPHAT)
        if analog(c.FOURTH_TOPHAT) < min_sensor_value_fourth:
            min_sensor_value_fourth = analog(c.FOURTH_TOPHAT)
        msleep(1)
    m.deactivate_motors()
    # If sensing black when it should be sensing white, increase bias
    # If sensing white when it should be sensing black, decrease bias
    c.LEFT_TOPHAT_BW = int(((max_sensor_value_left + min_sensor_value_left) / 2)) + big_tophat_bias
    c.RIGHT_TOPHAT_BW = int(((max_sensor_value_right + min_sensor_value_right) / 2)) + big_tophat_bias
    c.THIRD_TOPHAT_BW = int(((max_sensor_value_third + min_sensor_value_third) / 2)) + small_tophat_bias
    c.FOURTH_TOPHAT_BW = int(((max_sensor_value_fourth + min_sensor_value_fourth) / 2)) + small_tophat_bias
    avg_left_speed = total_left_speed / i
    avg_right_speed = total_right_speed / i
    c.BASE_LM_POWER = int(-avg_left_speed * 2)
    c.BASE_RM_POWER = int(-avg_right_speed * 2)
    c.FULL_LM_POWER = c.BASE_LM_POWER
    c.FULL_RM_POWER = c.BASE_RM_POWER
    c.HALF_LM_POWER = int(c.BASE_LM_POWER / 2)
    c.HALF_RM_POWER = int(c.BASE_RM_POWER / 2)
    c.MAX_TOPHAT_VALUE_RIGHT = max_sensor_value_right
    c.MIN_TOPHAT_VALUE_RIGHT = min_sensor_value_right
    c.MAX_TOPHAT_VALUE_LEFT = max_sensor_value_left
    c.MIN_TOPHAT_VALUE_LEFT = min_sensor_value_left
    c.MAX_TOPHAT_VALUE_THIRD = max_sensor_value_third
    c.MIN_TOPHAT_VALUE_THIRD = min_sensor_value_third
    print "Finished Calibrating. Moving back into starting box...\n"
    # Put commands here to get robot to desired starting position.


def shutdown(value = 256):
# Shuts down code without exit by default. Will exit if number is put in parantheses.
    print "Starting shutdown()"
    mav(c.LEFT_MOTOR, 0)
    mav(c.RIGHT_MOTOR, 0)
    msleep(25)
    ao()
    disable_servos()
    graphics_close()
    print "Shutdown complete\n"
    if value < 255:
        print "Exiting...\n"
        exit(value)


def sd(value = 86):
# Shortcut to end a run early.
    shutdown(value)

#--------------------Constant Changing Commands--------------

def halve_speeds():
    c.BASE_LM_POWER = c.HALF_LM_POWER
    c.BASE_RM_POWER = c.HALF_RM_POWER


def set_speeds_to(left_speed, right_speed):
    c.BASE_LM_POWER = left_speed
    c.BASE_RM_POWER = right_speed


def change_speeds_by_a_factor_of(speed_multiplier):
    c.BASE_LM_POWER = c.BASE_LM_POWER * speed_multiplier
    c.BASE_RM_POWER = c.BASE_RM_POWER * speed_multiplier


def normalize_speeds():
    c.BASE_LM_POWER = c.FULL_LM_POWER
    c.BASE_RM_POWER = c.FULL_RM_POWER

#-------------------------------Debug------------------------

def test_movement(exit = True):
# Used to see if movements and their defaults function as intended.
    print "Testing movement\n"
    m.turn_left()
    msleep(500)
    m.turn_right()
    msleep(500)
    m.drive(5000)
    msleep(500)  # Using msleep() instead of wait() to make sure each command turns off its wheels.
    m.backwards(5000)
    msleep(500)
    print "Testing complete."
    if exit == True:
        print "Exiting...\n"
        exit(86)


def test_servos(exit = True):
# Used to see if basic servo commands and constants function as intended.
    print "Testing servos\n"
    m.close_claw()
    m.stop_for(1000)  # Using wait() instead of msleep() to make sure wheels are off.
    m.open_claw()
    m.stop_for(1000)
    m.lift_arm()
    m.stop_for(1000)
    m.lower_arm()
    m.stop_for(1000)
    print "Testing complete."
    if exit == True:
        print "Exiting...\n"
        exit(86)