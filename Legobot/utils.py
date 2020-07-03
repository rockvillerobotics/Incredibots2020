import ctypes
KIPR=ctypes.CDLL("/usr/lib/libkipr.so")
import time as seconds
from objects import *
from decorators import *
import constants as c
import actions as a
import sensors as s
import movement as m

#-------------------------------States------------------------
# The left button no longer exists on the Wombat.

def is_button_pressed():
    return(KIPR.right_button() == 1)

def is_button_not_pressed():
    return(KIPR.right_button() == 0)

#-------------------------------Commands ------------------------
        
def stop_for(time=1000):  # Same as msleep command, but stops the wheels.
    m.deactivate_motors()
    KIPR.msleep(time)
    
    
def wait_until(boolean_function, time=c.SAFETY_TIME):
    if time == 0:
        time = c.SAFETY_TIME_NO_STOP
    sec = seconds.time() + time / 1000.0
    while seconds.time() < sec and not(boolean_function()):
        KIPR.msleep(1)

def always_true():
    return(True)

def always_false():
    return(False)
 
def wait_for_button():
    print("Press Right Button...")
    while isRightNotPressed():
        KIPR.msleep(1)
    print("Right button pressed\n")
    KIPR.msleep(500)


def setup():
    # Enables servos and sets up the robot for runs.
    print("Starting setup()")
    if IS_MAIN_BOT:
        print("I am the main bot")
    elif IS_CLONE_BOT:
        print("I am the clone bot")
    else:
        print("Error in bot determination")
        sd()
    KIPR.graphics_close()
    for motor in Motor.all_motors:
        KIPR.cmpc(motor.port)
    for servo in Servo.all_servos:
        KIPR.enable_servo(servo)
    KIPR.console_clear()
    print("Setup complete\n\n")


def calibrate_gcer(debug=False):
    calibrate_gyro()
    calibrate_tophats_and_motors()
    print("left_motor.base_power: " + str(left_motor.base_power))
    print("right_motor.base_power: " + str(right_motor.base_power))
    print("left.value_midpoint: " + str(left.value_midpoint))
    print("right.value_midpoint: " + str(right.value_midpoint))
    print("third.value_midpoint: " + str(third.value_midpoint))
    print("fourth.value_midpoint: " + str(fourth.value_midpoint))
    if debug == True:
        print("max_sensor_value_left: " + str(max_sensor_value_left))
        print("min_sensor_value_left: " + str(min_sensor_value_left))
        print("max_sensor_value_right: " + str(max_sensor_value_right))
        print("min_sensor_value_right: " + str(min_sensor_value_right))
        print("max_sensor_value_third: " + str(max_sensor_value_third))
        print("min_sensor_value_third: " + str(min_sensor_value_third))
        print("max_sensor_value_fourth: " + str(max_sensor_value_fourth))
        print("min_sensor_value_fourth: " + str(min_sensor_value_fourth))
    wait_until_round_starts()
    

def wait_until_round_starts(time=0):
    off(left_motor.port)
    off(right_motor.port)
    if time == 0:
        wait_for_light(c.LIGHT_SENSOR)
    else:
        msleep(time)


def calibrate_tophats(big_tophat_bias=-1000, small_tophat_bias=600):
    """Code to calibrate the tophat midpoint values."""
    # If sensing black when it should be sensing white, increase bias.
    # If sensing white when it should be sensing black, decrease bias.
    print("Running calibrate()")
    # Robot goes for a certain distance, based on the motors' "tics."
    left_motor.clear_tics()
    right_motor.clear_tics()
    m.activate_motors(int(-left_motor.base_power / 2), int(-right_motor.base_power / 2))
    while abs(left_motor.get_tics() + right_motor.get_tics()) / 2  < calibrate_tics:
        for tophat in Tophat.all_tophats:
            tophat.compare_and_replace_extremes()
        KIPR.msleep(1)
    m.deactivate_motors()
    for tophat in Tophat.all_tophats:
        if tophat.tophat_type == c.BIG_TOPHAT:
            tophat.determine_midpoint_from_extremes(big_tophat_bias)
        else:
            tophat.determine_midpoint_from_extremes(small_tophat_bias)
    print("Finished Calibrating. Moving back into starting box...\n")
    # Put commands here to get robot to desired starting position.


def calibrate_motors():
    print("Running calibrate()")
    # This initializes all variables to 0.
    angle, error, i, total_left_speed, total_right_speed = (0,)*5
    # Robot goes for a certain distance, based on the motors' "tics."
    left_motor.clear_tics()
    right_motor.clear_tics()
    m.activate_motors(int(-left_motor.base_power / 2), int(-right_motor.base_power / 2))
    while abs(left_motor.get_tics() + right_motor.get_tics()) / 2  < 1000:
        KIPR.msleep(10)
        angle += (s.get_change_in_angle() - gyro_bias) * 10
        error = 0.034470956 * angle  # Positive error means veering left. Negative means veering right.
        left_speed = (-left_motor.base_power + error) / 2
        right_speed = (-right_motor.base_power + error) / 2
        total_left_speed += left_speed
        total_right_speed += right_speed
        i += 1
        m.activate_motors(left_speed, right_speed)
    m.deactivate_motors()
    # All motor power variables are set based on the gyro drive in calibration.
    avg_left_speed = total_left_speed / i
    avg_right_speed = total_right_speed / i
    left_motor.set_all_powers(-avg_left_speed * 2)
    right_motor.set_all_powers(-avg_right_speed * 2)
    print("Finished Calibrating. Moving back into starting box...\n")
    # Put commands here to get robot to desired starting position.


def calibrate_tophats_and_motors(big_tophat_bias=-1000, small_tophat_bias=600):
    # Code to calibrate the tophat midpoint values and motor speeds that go straight.
    # If sensing black when it should be sensing white, increase bias
    # If sensing white when it should be sensing black, decrease bias
    print("Running calibrate()")
    angle = 0
    error = 0
    i = 0
    total_left_speed = 0
    total_right_speed = 0
    # Robot goes for a certain distance, based on the motors' "tics."
    left_motor.clear_tics()
    right_motor.clear_tics()
    m.activate_motors(int(-left_motor.base_power / 2), int(-right_motor.base_power / 2))
    while abs(left_motor.get_tics() + right_motors.get_tics()) / 2  < calibrate_tics:
        left_speed = (-left_motor.base_power + error) / 2
        right_speed = (-right_motor.base_power + error) / 2
        total_left_speed += left_speed
        total_right_speed += right_speed
        i += 1
        m.activate_motors(left_speed, right_speed)
        msleep(10)
        angle += (s.get_change_in_angle() - gyro_bias) * 10
        error = 0.034470956 * angle  # Positive error means veering left. Negative means veering right.
        # For all tophats, the sensor finds the maximum and minimum values it goes over during the calibration sequence.
        for tophat in Tophat.all_tophats:
            tophat.compare_and_replace_extremes()
    m.deactivate_motors()
    for tophat in Tophat.all_tophats:
        if tophat.tophat_type == c.BIG_TOPHAT:
            tophat.determine_midpoint_from_extremes(big_tophat_bias)
        else:
            tophat.determine_midpoint_from_extremes(small_tophat_bias)
    # All motor power variables are set based on the gyro drive in calibration.
    avg_left_speed = total_left_speed / i
    avg_right_speed = total_right_speed / i
    left_motor.set_all_powers(-avg_left_speed * 2)
    right_motor.set_all_powers(-avg_right_speed * 2)
    print("Finished Calibrating. Moving back into starting box...\n")
    # Put commands here to get robot to desired starting position.


def calibrate_gyro():
    ao()
    msleep(100)
    i = 0
    avg = 0
    while i < 100:
        avg = avg + s.get_change_in_angle()
        msleep(1)
        i = i + 1
    global gyro_bias
    gyro_bias = avg/i
    msleep(60)


def determine_gyro_conversion_rate():
    angle = 0
    print("Starting determine_gyro_conversion_rate()")
    print("Starting left.senses_white()")
    while left.senses_white():
        KIPR.msleep(10)
        angle += (s.get_change_in_angle() - gyro_bias) * 10
    print("Starting left.senses_black()")
    while left.senses_black():
        KIPR.msleep(10)
        angle += (s.get_change_in_angle() - gyro_bias) * 10
    print("Starting left.senses_white()")
    while left.senses_white():
        KIPR.msleep(10)
        angle += (s.get_change_in_angle() - gyro_bias) * 10
    print("Starting left.senses_black()")
    while left.senses_black():
        KIPR.msleep(10)
        angle += (s.get_change_in_angle() - gyro_bias) * 10
    print("Starting left.senses_white()")
    while left.senses_white():
        KIPR.msleep(10)
        angle += (s.get_change_in_angle() - gyro_bias) * 10
    "Stopping motors."
    m.deactivate_motors()
    c.DEGREE_CONVERSION_RATE = abs(angle / 360.0) #- 92
    print("DEGREE_CONVERSION_RATE: " + str(c.DEGREE_CONVERSION_RATE))


def shutdown(value = 256):
# Shuts down code without exit by default. Will exit if number is put in parantheses.
    print("Starting shutdown()")
    left_motor.set_power(0)
    right_motor.set_power(0)
    msleep(25)
    ao()
    disable_servos()
    graphics_close()
    print("Shutdown complete\n")
    if value < 255:
        print("Exiting...\n")
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

#----------------Screen Graphics-----------------

@print_function_name_with_arrows
def open_graphics_window():
    if not(c.IS_GRAPHICS_OPEN):
        console_clear()
        graphics_open(max_length, max_height) # Creates the graphics array with the given size
        graphics_fill(255, 255, 255)  # Fills screen with white          
    c.IS_GRAPHICS_OPEN = True


@print_function_name_with_arrows
def close_graphics_window():
    graphics_close()
    c.IS_GRAPHICS_OPEN = False


def graphics():
    console_clear()
    open_graphics_window()
    graphics_fill(255, 255, 255)  # Fills screen with white

    # Place graphics here.

    graphics_update()

#-------------------------------Debug------------------------

def test_movement(exit = True):
# Used to see if movements and their defaults function as intended.
    print("Testing movement\n")
    m.turn_left()
    msleep(500)
    m.turn_right()
    msleep(500)
    m.drive(5000)
    msleep(500)  # Using msleep() instead of wait() to make sure each command turns off its wheels.
    m.backwards(5000)
    msleep(500)
    print("Testing complete.")
    if exit == True:
        print("Exiting...\n")
        exit(86)


def test_servos(exit = True):
# Used to see if basic servo commands and constants function as intended.
    print("Testing servos\n")
    m.close_claw()
    m.stop_for(1000)  # Using wait() instead of msleep() to make sure wheels are off.
    m.open_claw()
    m.stop_for(1000)
    m.lift_arm()
    m.stop_for(1000)
    m.lower_arm()
    m.stop_for(1000)
    print("Testing complete.")
    if exit == True:
        print("Exiting...\n")
        exit(86)
