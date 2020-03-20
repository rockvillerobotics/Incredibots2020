from wallaby import *
import constants as c
import actions as a
import gyro as g
import sensors as s
import movement as m

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
        exit(86)
    if c.STARTING_CLAW_POS > c.MAX_SERVO_POS or c.STARTING_CLAW_POS < c.MIN_SERVO_POS or c.STARTING_ARM_POS > c.MAX_SERVO_POS or c.STARTING_ARM_POS < c.MIN_SERVO_POS:
        print "Invalid desired servo position\n"
        exit(86)
    graphics_close()
    cmpc(c.LEFT_MOTOR)
    cmpc(c.RIGHT_MOTOR)
    enable_servo(c.CLAW_SERVO)
    enable_servo(c.ARM_SERVO)
    enable_servo(c.MICRO_SERVO)
    m.move_claw(c.CLAW_CHECKING_POS, 8, 1)
    m.move_micro(c.MICRO_CHECKING_POS, 8, 1)
    m.move_claw(c.STARTING_CLAW_POS, 8, 1)
    m.move_arm(c.ARM_DOWN_POS, 8, 1)
    m.move_micro(c.STARTING_MICRO_POS, 8, 1)
    m.lower_ambulance_arm()
    msleep(25)
    ao()
    print "Set claw to starting position of %d" % c.STARTING_CLAW_POS
    print "Set arm to starting position of %d" % c.STARTING_ARM_POS
    console_clear()
    print "Setup complete\n\n"


def calibrate_regionals():
    msleep(100)
    g.calibrate_gyro()
    calibrate_tophats_and_motors()
    print "c.BASE_LM_POWER: " + str(c.BASE_LM_POWER)
    print "c.BASE_RM_POWER: " + str(c.BASE_RM_POWER)
    print "max_sensor_value_left: " + str(max_sensor_value_left)
    print "min_sensor_value_left: " + str(min_sensor_value_left)
    print "LEFT_TOPHAT_VALUE_MIDPOINT: " + str(c.LEFT_TOPHAT_VALUE_MIDPOINT)
    print "max_sensor_value_right: " + str(max_sensor_value_right)
    print "min_sensor_value_right: " + str(min_sensor_value_right)
    print "RIGHT_TOPHAT_VALUE_MIDPOINT: " + str(c.RIGHT_TOPHAT_VALUE_MIDPOINT)
    print "max_sensor_value_third: " + str(max_sensor_value_third)
    print "min_sensor_value_third: " + str(min_sensor_value_third)
    print "THIRD_TOPHAT_VALUE_MIDPOINT: " + str(c.THIRD_TOPHAT_VALUE_MIDPOINT)
    print "max_sensor_value_fourth: " + str(max_sensor_value_fourth)
    print "min_sensor_value_fourth: " + str(min_sensor_value_fourth)
    print "FOURTH_TOPHAT_BW: " + str(c.FOURTH_TOPHAT_BW)
    print "Seconds delay: " + str(c.SECONDS_DELAY)
    off(c.LEFT_MOTOR)
    off(c.RIGHT_MOTOR)
    wait_for_light(c.LIGHT_SENSOR)
    shut_down_in(118)  # URGENT: PUT BACK IN BEFORE COMPETITION


def calibrate_tophats(big_tophat_bias=-1000, small_tophat_bias=600):
    # Code to calibrate the bw values. This goes before every run. Ends with light sensor calibration.
    print "Running calibrate_tophats()"
    if c.IS_MAIN_BOT:
        calibrate_tics = 2100
    else: # Clone bot
        calibrate_tics = 3000
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
    m.activate_motors(int(-c.BASE_LM_POWER / 2), int(-c.BASE_RM_POWER / 2))
    # The calibration goes until the average tic count of the right and left motor are greater than the calibrate tics.
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
    c.LEFT_TOPHAT_VALUE_MIDPOINT = int(((max_sensor_value_left + min_sensor_value_left) / 2)) - 1000
    c.RIGHT_TOPHAT_VALUE_MIDPOINT = int(((max_sensor_value_right + min_sensor_value_right) / 2)) - 1000
    if c.IS_MAIN_BOT:
        c.THIRD_TOPHAT_VALUE_MIDPOINT = int(((max_sensor_value_third + min_sensor_value_third) / 2)) + 600
    else: # Clone bot
        c.THIRD_TOPHAT_VALUE_MIDPOINT = int(((max_sensor_value_third + min_sensor_value_third) / 2))
    c.FOURTH_TOPHAT_BW = int(((max_sensor_value_fourth + min_sensor_value_fourth) / 2))
    c.MAX_TOPHAT_VALUE_RIGHT = max_sensor_value_right
    c.MIN_TOPHAT_VALUE_RIGHT = min_sensor_value_right
    c.MAX_TOPHAT_VALUE_LEFT = max_sensor_value_left
    c.MIN_TOPHAT_VALUE_LEFT = min_sensor_value_left
    c.MAX_TOPHAT_VALUE_THIRD = max_sensor_value_third
    c.MIN_TOPHAT_VALUE_THIRD = min_sensor_value_third
    print "Finished Calibrating. Moving back into starting box...\n"
    # Put code to get back into the desired starting position.


def calibrate_tophats_and_motors():
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
    print "Running calibrate_tophats()"
    angle = 0
    error = 0
    i = 0
    total_left_speed = 0
    total_right_speed = 0
    total_seconds = 0
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
        intermediete_seconds = seconds()
        total_seconds += seconds() - intermediete_seconds
        msleep(1)
    m.deactivate_motors()
    # If sensing black when it should be sensing white, increase bias
    # If sensing white when it should be sensing black, decrease bias
    c.LEFT_TOPHAT_VALUE_MIDPOINT = int(((max_sensor_value_left + min_sensor_value_left) / 2)) - 1000
    c.RIGHT_TOPHAT_VALUE_MIDPOINT = int(((max_sensor_value_right + min_sensor_value_right) / 2)) - 1000
    if c.IS_MAIN_BOT:
        c.THIRD_TOPHAT_VALUE_MIDPOINT = int(((max_sensor_value_third + min_sensor_value_third) / 2)) + 600
    else: # Clone bot
        c.THIRD_TOPHAT_VALUE_MIDPOINT = int(((max_sensor_value_third + min_sensor_value_third) / 2))
    c.FOURTH_TOPHAT_BW = int(((max_sensor_value_fourth + min_sensor_value_fourth) / 2))
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


def shutdown(value=256):
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


def sd(value=86):
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

def test_movement(exit=True):
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


def test_servos(exit=True):
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