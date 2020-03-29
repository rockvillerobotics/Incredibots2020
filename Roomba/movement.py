from wombat import *
from decorators import *
from objects import *
import constants as c

#-----------------------------Base Commands-------------------------

def base_forward(speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * c.BASE_LM_POWER), int(speed_multiplier * c.BASE_RM_POWER))


def base_turn_left(speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * -1 * c.BASE_LM_POWER), int(speed_multiplier * c.BASE_RM_POWER))


def base_turn_right(speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * c.BASE_LM_POWER), int(speed_multiplier * -1 * c.BASE_RM_POWER))


def base_backwards(speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * -1 * c.BASE_LM_POWER), int(speed_multiplier * -1 * c.BASE_RM_POWER))


def base_veer_left(veer_multiplier=1, speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * veer_multiplier * 0.7 * c.BASE_LM_POWER), int(speed_multiplier * c.BASE_RM_POWER))


def base_veer_right(veer_multiplier=1, speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * c.BASE_LM_POWER), int(speed_multiplier * veer_multiplier * 0.7 * c.BASE_RM_POWER))

def base_veer(veer_multiplier_left=1, veer_multiplier_right=1, speed_multiplier=1.0):
    activate_motors(int(speed_multiplier * veer_multiplier_left * c.BASE_LM_POWER), int(speed_multiplier * veer_multiplier_right * c.BASE_RM_POWER))

#-----------------------------Basic Movement-------------------------

def activate_motors(left_motor_power=c.BASE_POWER, right_motor_power=c.BASE_POWER):
    if left_motor_power == c.BASE_POWER:
        left_motor_power = c.BASE_LM_POWER
    if right_motor_power == c.BASE_POWER:
        right_motor_power = c.BASE_RM_POWER
    if left_motor_power > 490:
        left_motor_power = 490
    elif left_motor_power < -490:
        left_motor_power = -490
    elif left_motor_power < 1 and left_motor_power >= 0:
        left_motor_power = 1
    elif left_motor_power > -1 and left_motor_power < 0:
        left_motor_power = -1
    if right_motor_power < -490:
        right_motor_power = -490
    elif right_motor_power > 490:
        right_motor_power = 490
    elif right_motor_power < 1 and right_motor_power >= 0:
        right_motor_power = 1
    elif right_motor_power > -1 and right_motor_power < 0:
        right_motor_power = -1
    if abs(left_motor_power - c.CURRENT_LM_POWER) > 150 or abs(right_motor_power - c.CURRENT_RM_POWER) > 150 or c.CURRENT_LM_POWER == 0 or c.CURRENT_RM_POWER == 0:
        left_velocity_change = (left_motor_power - c.CURRENT_LM_POWER) / 30
        right_velocity_change = (right_motor_power - c.CURRENT_RM_POWER) / 30
        while abs(c.CURRENT_LM_POWER - left_motor_power) > 10 and abs(c.CURRENT_RM_POWER - right_motor_power) > 10:
            create_drive_direct(int(c.CURRENT_LM_POWER), int(c.CURRENT_RM_POWER))
            c.CURRENT_LM_POWER += left_velocity_change
            c.CURRENT_RM_POWER += right_velocity_change
            msleep(1)
    create_drive_direct(int(left_motor_power), int(right_motor_power))
    c.CURRENT_LM_POWER = int(left_motor_power)
    c.CURRENT_RM_POWER = int(right_motor_power)


def deactivate_motors():
    create_stop()
    c.CURRENT_LM_POWER = 0
    c.CURRENT_RM_POWER = 0


def forward(time=c.DEFAULT_DRIVE_TIME, speed_multiplier=1.0):
    base_forward(speed_multiplier)
    print "Drive forward for %d ms" % time
    msleep(int(time))
    deactivate_motors()


def backwards(time=c.DEFAULT_BACKWARDS_TIME, speed_multiplier=1.0):
    base_backwards(speed_multiplier)
    print "Drive backwards for %d ms" % time
    msleep(int(time))
    deactivate_motors()


def turn_left(time=c.BASE_TIME, speed_multiplier=1.0):
    if time == c.BASE_TIME:
        time = c.LEFT_TURN_TIME
    base_turn_left(speed_multiplier)
    msleep(int(time))
    print "Turn left for %d ms" % time
    deactivate_motors()


def turn_right(time=c.BASE_TIME, speed_multiplier=1.0):
    if time == c.BASE_TIME:
        time = c.RIGHT_TURN_TIME
    base_turn_right(speed_multiplier)
    msleep(int(time))
    print "Turn right for %d ms" % time
    deactivate_motors()


def wait(time=1000):
    deactivate_motors()
    msleep(25)
    ao()
    msleep(time-25)


def av(motor_port, motor_power):
    # Moves one motor without affecting the other motor.
    if motor_port == c.LEFT_MOTOR:
        create_drive_direct(int(motor_power), int(c.CURRENT_RM_POWER))
        c.CURRENT_LM_POWER = int(motor_power)
    elif motor_port == c.RIGHT_MOTOR:
        create_drive_direct(int(c.CURRENT_LM_POWER), int(motor_power))
        c.CURRENT_RM_POWER = int(motor_power)
    else:
        print "Error in determining motor port for av()"
        msleep(2000)

#-----------------------------Servos----------------------------

def lift_arm(tics=3, ms=1, servo_position=c.ARM_UP_POS):
    print "Lifting servo to: %d" % servo_position
    arm_servo.move(servo_position, tics, ms)
    print "Arm reached up position: %d" % get_servo_position(c.ARM_SERVO)


def lower_arm(tics=3, ms=1, servo_position=c.ARM_DOWN_POS):
    print "Lowering arm to: %d" % servo_position
    arm_servo.move(servo_position, tics, ms)
    print "Arm reached down position: %d" % get_servo_position(c.ARM_SERVO)


def open_claw(tics=3, ms=1, servo_position=c.CLAW_OPEN_POS):
    print "Opening claw to: %d" % servo_position
    claw_servo.move(servo_position, tics, ms)
    print "Claw reached close position: %d" % get_servo_position(c.CLAW_SERVO)


def close_claw(tics=3, ms=1, servo_position=c.CLAW_CLOSE_POS):
    print "Closing claw to: %d" % servo_position
    claw_servo.move(servo_position, tics, ms)
    print "Claw reached close position: %d" % get_servo_position(c.CLAW_SERVO)
    