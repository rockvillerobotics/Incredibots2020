# Codes involving general motor or servo motion go here
from wallaby import *
from decorators import *
from objects import *
import constants as c
import gyro as g
import sensors as s

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

#------------------------------- No Print Movement -------------------------------
# These, as the name implies, do the same thing as the basic movement commands just without the prints.
# At one time, these were very useful commands. But, as time has gone on and techniques have been improved, they
# have become obsolete. We keep them as an archaic reference to what things used to be. We're nostalgic like that.

def drive_no_print(time=c.DEFAULT_DRIVE_TIME, should_stop=True, speed_multiplier=1.0):
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    base_drive(speed_multiplier)
    msleep(time)
    if should_stop:
        deactivate_motors()


def turn_left_no_print(time=c.LEFT_TURN_TIME, should_stop=True, speed_multiplier=1.0):
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    base_turn_left(speed_multiplier)
    msleep(time)
    if should_stop:
        deactivate_motors()


def turn_right_no_print(time=c.RIGHT_TURN_TIME, should_stop=True, speed_multiplier=1.0):
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    base_turn_right(speed_multiplier)
    msleep(time)
    if should_stop:
        deactivate_motors()


def backwards_no_print(time=c.DEFAULT_BACKWARDS_TIME, should_stop=True, speed_multiplier=1.0):
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    base_backwards(speed_multiplier)
    msleep(time)
    if should_stop:
        deactivate_motors()

#------------------------------- Basic Movement Commands -------------------------------
# These commands are really the building blocks of the whole code. They're practical; they're
# built to be used on a daily basis. If you're going to copy something of our code, I would suggest that it be this
# because these are better versions of the wallaby "mav".

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

def open_claw(tics=3, ms=1, servo_position=c.CLAW_OPEN_POS):
    print "Open claw to desired position: %d" % servo_position
    claw_servo.move(servo_pos, tics, ms)  # Checking for faulty values must go before setting position.
    print "Claw opened to position: %d" % get_servo_position(c.CLAW_SERVO)


def close_claw(tics=3, ms=1, servo_pos=c.CLAW_CLOSE_POS):
    print "Close claw to desired position: %d" % servo_position
    claw_servo.move(servo_pos, tics, ms)
    print "Claw closed to position: %d" % get_servo_position(c.CLAW_SERVO)


def lift_arm(tics=3, ms=1, servo_pos=c.ARM_UP_POS):
    print "Set arm servo to desired up position: %d" % servo_position
    arm_servo.move(servo_pos, tics, ms)
    print "Arm reached up position: %d" % get_servo_position(c.ARM_SERVO)


def lower_arm(tics=3, ms=1, servo_pos=c.BASE_TIME):
    print "Set arm servo to desired down position: %d" % servo_position
    if servo_position == c.BASE_TIME:
        servo_position = c.ARM_DOWN_POS
    arm_servo.move(servo_pos, tics, ms)
    print "Arm reached down position: %d" % get_servo_position(c.ARM_SERVO)

#------------------------------ Servo Motors -------------------------------
# All these commands move the motors to a specified location at a specified speed.
# The more tics per second, the faster the motors moves.

@print_function_name_with_arrows
def lift_ambulance_arm(desired_speed=c.BASE_AMBULANCE_ARM_POWER):
    move_ambulance_arm(c.AMBULANCE_ARM_HIGH_POS, desired_speed)


@print_function_name_with_arrows
def lower_ambulance_arm(desired_speed=c.BASE_AMBULANCE_ARM_POWER):
    if s.isLeftLimitSwitchNotPressed():
        mav(c.AMBULANCE_ARM_MOTOR, -c.BASE_AMBULANCE_ARM_POWER)
        s.wait_until_limit_switch_is_pressed()
        mav(c.AMBULANCE_ARM_MOTOR, 0)
    cmpc(c.AMBULANCE_ARM_MOTOR)
    #move_ambulance_arm(c.AMBULANCE_ARM_LOW_POS, desired_speed)


@print_function_name_with_arrows
def move_ambulance_arm(desired_tic_location, desired_speed=c.BASE_AMBULANCE_ARM_POWER):
    move_motor(c.AMBULANCE_ARM_MOTOR, desired_tic_location, desired_speed)


@print_function_name_with_arrows
def move_motor(motor_port, desired_tic_location, desired_speed):
    # 2047 tics in 360 degrees
    # while desired_tic_location > 2047:
    #    desired_tic_location -= 2047
    # while desired_tic_location < 0:
    #    desired_tic_location += 2047
    if desired_tic_location - get_motor_tics(motor_port) > 0:
        desired_speed = desired_speed
    elif desired_tic_location - get_motor_tics(motor_port) < 0:
        desired_speed = -desired_speed
    else:
        print "Boi you're bad. The desired location and the current location are the same."
    print "Current tic location: " + str(get_motor_tics(c.AMBULANCE_ARM_MOTOR))
    print "Desired tic location: " + str(desired_tic_location)
    sec = seconds() + 2000 / 1000.0
    while seconds() < sec and abs(desired_tic_location - get_motor_tics(motor_port)) > 5:
        speed = (desired_tic_location - get_motor_tics(motor_port)) * 20
        if speed > desired_speed:
            speed = desired_speed
        elif speed < desired_speed:
            speed = desired_speed
        elif speed >= 0 and speed < 11:
            speed = 11
        elif speed < 0 and speed > -11:
            speed = -11
        mav(motor_port, speed)
        msleep(1)
    mav(motor_port, 0)


#------------------------------- Bump Sensors -------------------------------

def bumpPressedRight():
    return(digital(c.RIGHT_BUMP_SENSOR) == 1)

def notBumpPressedRight():
    return(digital(c.RIGHT_BUMP_SENSOR) == 0)


def base_bumpfollow_right():
    if bumpPressedRight():
        activate_motors(c.LFOLLOW_SMOOTH_LM_POWER, right_motor.base_power)
    else:
        activate_motors(left_motor.base_power, c.LFOLLOW_SMOOTH_RM_POWER)
    msleep(1)
    g.update_gyro()


@print_function_name_with_arrows
def bumpfollow_right_until_black_left(time=c.SAFETY_TIME, should_stop=True):
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    sec = seconds() + time / 1000.0
    while seconds() < sec and s.isLeftOnWhite():
        base_bumpfollow_right()
    if should_stop:
        deactivate_motors()


@print_function_name_with_arrows
def bumpfollow_right_until_white_left(time=c.SAFETY_TIME, should_stop=True):
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    sec = seconds() + time / 1000.0
    while seconds() < sec and s.isLeftOnBlack():
        base_bumpfollow_right()
    if should_stop:
        deactivate_motors()


@print_function_name_with_arrows
def bumpfollow_right_until_black_right(time=c.SAFETY_TIME, should_stop=True):
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    sec = seconds() + time / 1000.0
    while seconds() < sec and s.isRightOnWhite():
        base_bumpfollow_right()
    if should_stop:
        deactivate_motors()


@print_function_name_with_arrows
def bumpfollow_right_until_white_right(time=c.SAFETY_TIME, should_stop=True):
    if time == 0:
        should_stop = False
        time = c.SAFETY_TIME
    sec = seconds() + time / 1000.0
    while seconds() < sec and s.isRightOnBlack():
        base_bumpfollow_right()
    if should_stop:
        deactivate_motors()
