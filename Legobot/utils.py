from wallaby import *
import constants as c
import actions as a
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
        sd()
    graphics_close()
    for motor in Motor.all_motors:
        cmpc(motor)
    for servo in Servo.all_servos:
        enable_servo(servo)
    console_clear()
    print "Setup complete\n\n"


def calibrate_regionals(debug=False):
    g.calibrate_gyro()
    calibrate_tophats_and_motors()
    print "left_motor.base_power: " + str(left_motor.base_power)
    print "right_motor.base_power: " + str(right_motor.base_power)
    print "left.value_midpoint: " + str(left.value_midpoint)
    print "right.value_midpoint: " + str(right.value_midpoint)
    print "third.value_midpoint: " + str(third.value_midpoint)
    print "fourth.value_midpoint: " + str(fourth.value_midpoint)
    if debug == True:
        print "max_sensor_value_left: " + str(max_sensor_value_left)
        print "min_sensor_value_left: " + str(min_sensor_value_left)
        print "max_sensor_value_right: " + str(max_sensor_value_right)
        print "min_sensor_value_right: " + str(min_sensor_value_right)
        print "max_sensor_value_third: " + str(max_sensor_value_third)
        print "min_sensor_value_third: " + str(min_sensor_value_third)
        print "max_sensor_value_fourth: " + str(max_sensor_value_fourth)
        print "min_sensor_value_fourth: " + str(min_sensor_value_fourth)
    msleep(1000)
    

def wait_until_round_starts(time=0):
    off(left_motor.port)
    off(right_motor.port)
    if time == 0:
        wait_for_light(c.LIGHT_SENSOR)
    else:
        msleep(time)
    


def calibrate_tophats(big_tophat_bias=-1000, small_tophat_bias=600):
    # Code to calibrate the bw values. This goes before every run. Ends with light sensor calibration.
    max_sensor_value_right = 0
    min_sensor_value_right = 90000
    max_sensor_value_left = 0
    min_sensor_value_left = 90000
    max_sensor_value_third = 0
    min_sensor_value_third = 90000
    max_sensor_value_fourth = 0
    min_sensor_value_fourth = 90000
    left_motor.clear_tics()
    right_motor.clear_tics()
    if c.IS_MAIN_BOT:
        calibrate_tics = 2100
    else: # Clone bot
        calibrate_tics = 3000
    print "Running calibrate()"
    m.activate_motors(int(-left_motor.base_power / 2), int(-right_motor.base_power / 2))
    while abs(left_motor.get_tics() + right_motor.get_tics()) / 2  < calibrate_tics:
        if analog(left.port) > max_sensor_value_left:
            max_sensor_value_left = analog(left.port)
        elif analog(left.port) < min_sensor_value_left:
            min_sensor_value_left = analog(left.port)
        if analog(right.port) > max_sensor_value_right:
            max_sensor_value_right = analog(right.port)
        elif analog(right.port) < min_sensor_value_right:
            min_sensor_value_right = analog(right.port)
        if analog(third.port) > max_sensor_value_third:
            max_sensor_value_third = analog(third.port)
        elif analog(third.port) < min_sensor_value_third:
            min_sensor_value_third = analog(third.port)
        if analog(fourth.port) > max_sensor_value_fourth:
            max_sensor_value_fourth = analog(fourth.port)
        elif analog(fourth.port) < min_sensor_value_fourth:
            min_sensor_value_fourth = analog(fourth.port)
        msleep(1)
    m.deactivate_motors()
    # If sensing black when it should be sensing white, increase bias
    # If sensing white when it should be sensing black, decrease bias
    left.set_value_midpoint(int(((max_sensor_value_left + min_sensor_value_left) / 2)) + big_tophat_bias)
    right.set_value_midpoint(int(((max_sensor_value_right + min_sensor_value_right) / 2)) + big_tophat_bias)
    third.set_value_midpoint(int(((max_sensor_value_third + min_sensor_value_third) / 2)) + small_tophat_bias)
    fourth.set_value_midpoint(int(((max_sensor_value_fourth + min_sensor_value_fourth) / 2)) + small_tophat_bias)
    left.set_black_value(max_sensor_value_left)
    left.set_white_value(min_sensor_value_left)
    right.set_black_value(max_sensor_value_right)
    right.set_white_value(min_sensor_value_right)
    third.set_black_value(max_sensor_value_third)
    third.set_white_value(min_sensor_value_third)
    fourth.set_black_value(max_sensor_value_fourth)
    fourth.set_white_value(min_sensor_value_fourth)
    print "Finished Calibrating. Moving back into starting box...\n"
    # Put commands here to get robot to desired starting position.


def calibrate_motors():
    left_motor.clear_tics()
    right_motor.clear_tics()
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
    m.activate_motors(int(-left_motor.base_power / 2), int(-right_motor.base_power / 2))
    while abs(left_motor.get_tics() + right_motors.get_tics()) / 2  < calibrate_tics:
        msleep(10)
        angle += (g.get_change_in_angle() - g.bias) * 10
        error = 0.034470956 * angle  # Positive error means veering left. Negative means veering right.
        left_speed = (-left_motor.base_power + error) / 2
        right_speed = (-right_motor.base_power + error) / 2
        total_left_speed += left_speed
        total_right_speed += right_speed
        i += 1
        m.activate_motors(left_speed, right_speed)
    m.deactivate_motors()
    # Set all motor powers based on gyro drive during the calibrate.
    avg_left_speed = total_left_speed / i
    avg_right_speed = total_right_speed / i
    left_motor.set_base_power(-avg_left_speed * 2)
    right_motor.set_base_power(-avg_right_speed * 2)
    left_motor.set_half_power(left_motor.base_power / 2)
    right_motor.set_half_power(right_motor.base_power / 2)
    left_motor.set_full_power(left_motor.base_power)
    right_motor.set_full_power(right_motor.base_power)
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
    left_motor.clear_tics()
    right_motor.clear_tics()
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
    m.activate_motors(int(-left_motor.base_power / 2), int(-right_motor.base_power / 2))
    while abs(left_motor.get_tics() + right_motors.get_tics()) / 2  < calibrate_tics:
        left_speed = (-left_motor.base_power + error) / 2
        right_speed = (-right_motor.base_power + error) / 2
        total_left_speed += left_speed
        total_right_speed += right_speed
        i += 1
        m.activate_motors(left_speed, right_speed)
        msleep(10)
        angle += (g.get_change_in_angle() - g.bias) * 10
        error = 0.034470956 * angle  # Positive error means veering left. Negative means veering right.
        if analog(right.port) > max_sensor_value_right:
            max_sensor_value_right = analog(right.port)
        if analog(right.port) < min_sensor_value_right:
            min_sensor_value_right = analog(right.port)
        if analog(left.port) > max_sensor_value_left:
            max_sensor_value_left = analog(left.port)
        if analog(left.port) < min_sensor_value_left:
            min_sensor_value_left = analog(left.port)
        if analog(third.port) > max_sensor_value_third:
            max_sensor_value_third = analog(third.port)
        if analog(third.port) < min_sensor_value_third:
            min_sensor_value_third = analog(third.port)
        if analog(fourth.port) > max_sensor_value_fourth:
            max_sensor_value_fourth = analog(fourth.port)
        if analog(fourth.port) < min_sensor_value_fourth:
            min_sensor_value_fourth = analog(fourth.port)
        msleep(1)
    m.deactivate_motors()
    # If sensing black when it should be sensing white, increase bias
    # If sensing white when it should be sensing black, decrease bias
    left.set_value_midpoint(int(((max_sensor_value_left + min_sensor_value_left) / 2)) + big_tophat_bias)
    right.set_value_midpoint(int(((max_sensor_value_right + min_sensor_value_right) / 2)) + big_tophat_bias)
    third.set_value_midpoint(int(((max_sensor_value_third + min_sensor_value_third) / 2)) + small_tophat_bias)
    fourth.set_value_midpoint(int(((max_sensor_value_fourth + min_sensor_value_fourth) / 2)) + small_tophat_bias)
    left.set_black_value(max_sensor_value_left)
    left.set_white_value(min_sensor_value_left)
    right.set_black_value(max_sensor_value_right)
    right.set_white_value(min_sensor_value_right)
    third.set_black_value(max_sensor_value_third)
    third.set_white_value(min_sensor_value_third)
    fourth.set_black_value(max_sensor_value_fourth)
    fourth.set_white_value(min_sensor_value_fourth)
    # Set all motor powers based on gyro drive during the calibrate.
    avg_left_speed = total_left_speed / i
    avg_right_speed = total_right_speed / i
    left_motor.set_base_power(-avg_left_speed * 2)
    right_motor.set_base_power(-avg_right_speed * 2)
    left_motor.set_half_power(left_motor.base_power / 2)
    right_motor.set_half_power(right_motor.base_power / 2)
    left_motor.set_full_power(left_motor.base_power)
    right_motor.set_full_power(right_motor.base_power)
    print "Finished Calibrating. Moving back into starting box...\n"
    # Put commands here to get robot to desired starting position.


def shutdown(value = 256):
# Shuts down code without exit by default. Will exit if number is put in parantheses.
    print "Starting shutdown()"
    left_motor.set_power(0)
    right_motor.set_power(0)
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
    left_motor.set_base_power(left_motor.half_power)
    right_motor.set_base_pwoer(right_motor.half_power)


def set_speeds_to(left_speed, right_speed):
    left_motor.set_base_power(left_speed)
    right_motor.set_base_pwoer(right_speed)


def change_speeds_by_a_factor_of(speed_multiplier):
    left_motor.set_base_power(left_motor.base_power * speed_multiplier)
    right_motor.set_base_power(right_motor.base_power * speed_multiplier)


def normalize_speeds():
    left_motor.set_base_power(left_motor.full_power)
    right_motor.set_base_pwoer(right_motor.full_power)

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