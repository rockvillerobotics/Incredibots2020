import ctypes
KIPR=ctypes.CDLL("/usr/lib/libkipr.so")
import time as seconds
import constants as c
import objects as o
import movement as m

class Gyro:
    
    def __init__(self, get_angle_function):
        self.get_angle_function = get_angle_function
        self.bias = 0
        # The degree conversion rate is set to a roughly correct value in case
        # "determine_gyro_conversion_rate" is not run.
        self.degree_conversion_rate = 6281.8888889
    
    def get_change_in_angle(self):
        return(self.get_angle_function())

    #-----------------------Calibration Commands-------------------------------------

    def zero_gyro(self):
        """ 'Zeroes' the gyro sensor. It determines what the gyro reads when the bot is resting.
        """
        i = 0
        avg = 0
        while i < 100:
            avg = avg + self.get_change_in_angle()
            msleep(1)
            i = i + 1
        self.bias = avg/i
        msleep(60)


    def determine_gyro_conversion_rate(self):
        """ Figures out how many degrees the gyro sensor counts during 
        a 360 degree turn and uses that as a basis for all other turns.
        Must have at least 1 tophat initialized.
        """
        angle = 0
        while o.Tophat.allTophats[0].senses_white():
            msleep(10)
            angle += (self.get_change_in_angle() - self.bias) * 10
        while o.Tophat.allTophats[0].senses_white():
            msleep(10)
            angle += (self.get_change_in_angle() - self.bias) * 10
        while o.Tophat.allTophats[0].senses_white():
            msleep(10)
            angle += (self.get_change_in_angle() - self.bias) * 10
        while o.Tophat.allTophats[0].senses_white():
            msleep(10)
            angle += (self.get_change_in_angle() - self.bias) * 10
        while o.Tophat.allTophats[0].senses_white():
            msleep(10)
            angle += (self.get_change_in_angle() - self.bias) * 10
        m.deactivate_motors()
        self.degree_conversion_rate = abs(angle / 360.0)
        print("degree_conversion_rate: " + str(self.degree_conversion_rate))
        
    def calibrate_motor_powers(self):
        """ Has the robot drive straight using the gyro sensor 
        and sets those to be motors' base powers.
        """
        angle = 0
        error = 0
        i = 0
        total_left_speed = 0
        total_right_speed = 0
        sec = seconds() + 3
        while seconds() < sec:
            left_speed = c.BASE_LM_POWER + error
            right_speed = c.BASE_RM_POWER + error
            total_left_speed += left_speed
            total_right_speed += right_speed
            i += 1
            m.activate_motors(left_speed, right_speed)
            msleep(10)
            angle += (self.get_change_in_angle() - self.bias) * 10
            error = 0.034470956 * angle  # Positive error means veering left. Negative means veering right.
        m.deactivate_motors()
        avg_left_speed = total_left_speed / i
        avg_right_speed = total_right_speed / i
        o.Motor.all_motors[0].set_reference_powers(int(avg_left_speed))
        o.Motor.all_motors[1].set_reference_powers(int(avg_right_speed))
        print("left_motor.base_power: " + str(o.Motor.all_motors[0].base_power))
        print("right_motor.base_power: " + str(o.Motor.all_motors[1].base_power))

#-----------------------Gyro-Based Movement Commands-------------------------------------
# The gyro sensor can determine what angle the robot is at any given point in time. So, if the gyro sensor senses
# an angle other than 0, then it is clear that the bot is veering. So, the robot veers in the opposite direction to
# reduce the error proportionally to how big the error is.

    @print_function_name_with_arrows
    def drive_gyro_until(self, boolean_function, *, time=c.SAFETY_TIME, should_stop=True):
        if time == 0:
            should_stop = False
            time = c.SAFETY_TIME
        angle = 0
        error = 0
        memory = 0
        sec = seconds() + time / 1000.0
        while seconds() < sec and not(boolean_function()):
            left_speed = o.Motor.allMotors[0].base_power - (error + memory) 
            right_speed = o.Motor.allMotors[1].base_power + error + memory
            m.activate_motors(left_speed, right_speed)
            msleep(10)
            angle += (self.get_change_in_angle() - self.bias) * 10
            error = 0.034470956 * angle  # Positive error means veering left. Negative means veering right.
            memory += 0.00001 * error
        if should_stop:
            m.deactivate_motors()
        
        
    @print_function_name_with_arrows
    def backwards_gyro_until(self, boolean_function, *, time=c.SAFETY_TIME, should_stop=True):
        angle = 0
        error = 0
        memory = 0
        if time == 0:
            should_stop = False
            time = c.SAFETY_TIME
        sec = seconds() + time / 1000.0
        while seconds() < sec and not(boolean_function()):
            left_speed = -(o.Motor.allMotors[0].base_power - (error + memory))
            right_speed = -(o.Motor.allMotors[1].base_power + error + memory)
            m.activate_motors(left_speed, right_speed)
            msleep(10)
            angle += (self.get_change_in_angle() - self.bias) * 10
            error = 0.034470956 * angle  # Positive error means veering left. Negative means veering right.
            memory += 0.001 * error
        if should_stop:
            m.deactivate_motors()
            
    #-----------------------Gyro-Based Turning Commands-------------------------------------
    # The robot turns until the gyro sensor senses the desired angle.

    def turn_gyro(self, degrees, should_stop=True):
        angle = 0
        target_angle = degrees * c.DEGREE_CONVERSION_RATE
        if target_angle > 0:
            m.base_turn_left()
            sec = seconds() + c.SAFETY_TIME
            while angle < target_angle and seconds() < sec:
                msleep(10)
                angle += (self.get_change_in_angle() - self.bias) * 10
        else:
            m.base_turn_right()
            sec = seconds() + c.SAFETY_TIME
            while angle > target_angle and seconds() < sec:
                msleep(10)
                angle += (self.get_change_in_angle() - self.bias) * 10
        if should_stop:
            m.deactivate_motors()


    def turn_left_gyro(self, degrees=90, should_stop=True):
        print("Starting turn_left_gyro() for " + str(degrees) + " degrees")
        self.turn_gyro(degrees, should_stop)


    def turn_right_gyro(self, degrees=90, should_stop=True):
        print("Starting turn_right_gyro() for " + str(degrees) + " degrees")
        self.turn_gyro(-degrees, should_stop)

        
