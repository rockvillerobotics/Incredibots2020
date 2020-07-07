import ctypes
KIPR=ctypes.CDLL("/usr/lib/libkipr.so")
import time as seconds
import constants as c
import objects as o
import Motor as M

class Tophat:
    
    refresh_rate = 30
    all_tophats = []
    
    # An enumerator for the different line follow modes.
    
    def __init__(self, port, location, tophat_type):
        self.port = port
        self.value_midpoint = 1000
        # These values don't work unless the robot is calibrated.
        self.black_value = 0
        self.white_value = 9999
        self.side = location[0]
        self.direction = location[1]
        self.tophat_type = tophat_type
        Tophat.all_tophats.append(self)

    def get_value(self):
        return KIPR.analog(self.port)

    def get_value_midpoint(self):
        return KIPR.self.value_midpoint

    def senses_black(self):
        return self.get_value() < self.value_midpoint

    def senses_white(self):
        return self.get_value() > self.value_midpoint

    def compare_and_replace_extremes(self):
        if self.get_value() > self.black_value:
            self.black_value = self.get_value()
        elif self.get_value() < self.white_value:
            self.white_value = self.get_value()

    def determine_midpoint_from_extremes(self, bias):
        self.set_value_midpoint((self.black_value + self.white_value) / 2 + bias)

    def lfollow(self, time, mode=c.STANDARD, should_stop=True, bias=0):
        target = 100.0 * (self.value_midpoint - self.white_value) / (self.black_value - self.white_value) + bias
        last_error = 0
        integral = 0
        sec = seconds.time() + time / 1000.0
        while seconds.time() < sec:
            norm_reading = 100.0 * (self.get_value() - self.white_value) / (self.black_value - self.white_value)
            error = target - norm_reading       # Positive error means white, negative means black.
            derivative = error - last_error     # If rate of change is going negative, need to veer left
            last_error = error
            integral = 0.5 * integral + error
            if error > 30 or error < -30:
                kp = 15
                ki = c.KI
                kd = c.KD
            elif error < 10 and error > -10:
                kp = 2 * 1.2
                ki = c.KI / 10
                kd = c.KD / 10
            else:
                kp = 4 * 1.2
                ki = c.KI / 2
                kd = c.KD / 2
            if mode == c.STANDARD:
                left_power = o.left_motor.base_power - ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
                right_power = o.right_motor.base_power + ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
            elif mode == c.INSIDE_LINE:
                left_power = o.left_motor.base_power + ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
                right_power = o.right_motor.base_power - ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
            M.Motor.activate_motors(left_power * self.direction, right_power * self.direction)
            KIPR.msleep(10)
        if should_stop:
            M.Motor.deactivate_motors()

    def lfollow_until(self, boolean_function, mode=c.STANDARD, should_stop=True, bias=0, *, time=c.SAFETY_TIME):
        target = 100.0 * (self.value_midpoint - self.white_value) / (self.black_value - self.white_value) + bias
        last_error = 0
        integral = 0
        sec = seconds.time() + time / 1000.0
        while seconds.time() < sec and not(boolean_function()):
            norm_reading = 100.0 * (self.get_value() - self.white_value) / (self.black_value - self.white_value)
            error = target - norm_reading       # Positive error means white, negative means black.
            derivative = error - last_error     # If rate of change is going negative, need to veer left
            last_error = error
            integral = 0.5 * integral + error
            if error > 30 or error < -30:
                kp = 15
                ki = c.KI
                kd = c.KD
            elif error < 10 and error > -10:
                kp = 2 * 1.2
                ki = c.KI / 10
                kd = c.KD / 10
            else:
                kp = 4 * 1.2
                ki = c.KI / 2
                kd = c.KD / 2
            if mode == c.STANDARD:
                left_power = o.left_motor.base_power - ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
                right_power = o.right_motor.base_power + ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
            elif mode == c.INSIDE_LINE:
                left_power = o.left_motor.base_power + ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
                right_power = o.right_motor.base_power - ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
            M.Motor.activate_motors(left_power * self.direction, right_power * self.direction)
            KIPR.msleep(10)
        if should_stop:
            M.Motor.deactivate_motors()

    def lfollow_choppy(self, time, should_stop=True):
        left_motor = M.Motor.all_motors[0]
        right_motor = M.Motor.all_motors[1]
        sec = seconds.time() + time / 1000.0
        while seconds.time() < sec:
            if self.senses_black():
                left_motor.stop()
                right_motor.accelerate_to(right_motor.base_power)
            elif self.senses_white():
                left_motor.stop()
                right_motor.accelerate_to(right_motor.base_power)
            KIPR.msleep(30)
        if should_stop:
            M.Motor.deactivate_motors()
