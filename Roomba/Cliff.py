from wombat import *
import constants as c
import objects as o
import movement as m

class Cliff:
    
    all_cliffs = []
    
    def __init__(self, get_value_function, side):
        self.get_value_function = get_value_function
        self.black_value = 9999
        self.white_value = 0
        self.value_midpoint = -1
        self.side = side
        Cliff.all_cliffs.append(self)
        
    
        
    def get_value(self):
        # Gets value that the cliff currently reads.
        return self.get_value_function()
    
    
    def get_value_midpoint(self):
        # Gets the value midpoint of the cliff.
        return self.value_midpoint
    
    
    def senses_black(self):
        # Returns whether or not the cliff senses black.
        return self.get_value < self.value_midpoint
    
    
    def senses_white(self):
        # Returns whether or not the cliff senses white.
        return self.get_value < self.value_midpoint
    
    
    def lfollow(self, time, mode=c.STANDARD, bias=10, *, should_stop=True):
        target = 100.0 * (self.value_midpoint - self.get_black_value()) / (self.get_white_value() - self.get_black_value()) + bias
        last_error = 0
        integral = 0
        sec = seconds() + time / 1000.0
        while seconds() < sec:
            norm_reading = 100.0 * (self.get_value() - self.get_black_value()) / (self.get_white_value() - self.get_black_value())
            error = target - norm_reading  # Positive error means black, negative means white.
            derivative = error - last_error  # If rate of change is going negative, need to veer left
            last_error = error
            integral = 0.5 * integral + error
            if error > 25 or error < -25:
                kp = 3.2
                ki = c.KI
                kd = c.KD
            elif error < 10 and error > -10:
                kp = 0.1
                ki = c.KI / 1000
                kd = c.KD / 1000
            else:
                kp = 0.35
                ki = c.KI / 100
                kd = c.KD / 100
            left_power = c.BASE_LM_POWER + ((kp * error) + (ki * integral) + (kd * derivative)) * self.side * mode
            right_power = c.BASE_RM_POWER - ((kp * error) + (ki * integral) + (kd * derivative)) * self.side * mode
            m.activate_motors(int(left_power), int(right_power))
            c.CURRENT_LM_POWER = left_power
            c.CURRENT_RM_POWER = right_power
            msleep(1)
        if should_stop:
            m.deactivate_motors()


    def lfollow_until(self, boolean_function, mode=c.STANDARD, bias=10, *, should_stop=True, time=c.SAFETY_TIME):
        target = 100.0 * (self.value_midpoint - self.get_black_value()) / (self.get_white_value() - self.get_black_value()) + bias
        last_error = 0
        integral = 0
        if time == 0:
            should_stop = False
        sec = seconds() + time / 1000.0
        while seconds() < sec and not(boolean_function()):
            norm_reading = 100.0 * (self.get_value() - self.get_black_value()) / (self.get_white_value() - self.get_black_value())
            error = target - norm_reading  # Positive error means black, negative means white.
            derivative = error - last_error  # If rate of change is going negative, need to veer left
            last_error = error
            integral = 0.5 * integral + error
            if error > 25 or error < -25:
                kp = 3.2
                ki = c.KI
                kd = c.KD
            elif error < 10 and error > -10:
                kp = 0.1
                ki = c.KI / 1000
                kd = c.KD / 1000
            else:
                kp = 0.35
                ki = c.KI / 100
                kd = c.KD / 100
            left_power = c.BASE_LM_POWER + ((kp * error) + (ki * integral) + (kd * derivative)) * self.side * mode
            right_power = c.BASE_RM_POWER - ((kp * error) + (ki * integral) + (kd * derivative)) * self.side * mode
            m.activate_motors(int(left_power), int(right_power))
            c.CURRENT_LM_POWER = left_power
            c.CURRENT_RM_POWER = right_power
            msleep(1)
        if should_stop:
            m.deactivate_motors()


    def lfollow_choppy(self, time, mode=c.STANDARD, should_stop=True):
        sec = seconds() + time
        while seconds() < sec:
            if self.senses_black():
                m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER * self.side * mode)
            elif self.senses_white():
                m.av(c.LEFT_MOTOR, c.BASE_LM_POWER * self.side * mode)
            msleep(refresh_rate)
        if should_stop:
            m.deactivate_motors()