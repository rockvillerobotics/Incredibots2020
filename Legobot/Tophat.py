from wombat import *
import constants as c
import objects as o
import movement as m

class Tophat:
    refresh_rate = 30
    
    # An enumerator for the different line follow modes.
    class Mode:
        # We use auto() since we don't care what the exact literal is.
        STANDARD = auto()
        INSIDE_LINE = auto()
        
    
    def __init__(self, port, location):
        self.port = port
        self.value_midpoint = 1000
        self.black_value = 3200
        self.white_value = 128
        self.side = location[1]
        self.direction = location[2]


    def set_value_midpoint(self, value_midpoint):
        self.value_midpoint = value_midpoint
        
    
    def set_black_value(self, black_value):
        self.black_value = black_value
    
    
    def set_white_value(self, white_value):
        self.white_value = white_value
        
    def senses_black(self):
        return analog(self.port) < self.value_midpoint
    
    
    def senses_white(self):
        return analog(self.port) > self.value_midpoint
    
    
    def lfollow(self, time, mode=Mode.STANDARD, should_stop=True, bias=0):
        target = 100.0 * (self.value_midpoint - self.white_value) / (self.black_value - self.white_value) + bias
        last_error = 0
        integral = 0
        sec = seconds() + time / 1000.0
        while seconds() < sec:
            norm_reading = 100.0 * (analog(self.port) - self.white_value) / (self.black_value - self.white_value)
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
            if mode == Mode.STANDARD:
                left_power = o.left_motor.base_power - ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
                right_power = o.right_motor.base_power + ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
            elif mode == Mode.INSIDE_LINE:
                left_power = o.left_motor.base_power + ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
                right_power = o.right_motor.base_power - ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
            m.activate_motors(left_power * self.direction, right_power * self.direction)
            msleep(10)
        if should_stop:
            m.deactivate_motors()

    
    def lfollow_until(self, boolean_function, mode=Mode.STANDARD, should_stop=True, bias=0, *, time=c.SAFETY_TIME):
        target = 100.0 * (self.value_midpoint - self.white_value) / (self.black_value - self.white_value) + bias
        last_error = 0
        integral = 0
        sec = seconds() + time / 1000.0
        while seconds() < sec and not(boolean_function()):
            norm_reading = 100.0 * (analog(self.port) - self.white_value) / (self.black_value - self.white_value)
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
            if mode == Mode.STANDARD:
                left_power = o.left_motor.base_power - ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
                right_power = o.right_motor.base_power + ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
            elif mode == Mode.INSIDE_LINE:
                left_power = o.left_motor.base_power + ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
                right_power = o.right_motor.base_power - ((kp * error) + (ki * integral) + (kd * derivative)) * self.side
            m.activate_motors(left_power * self.direction, right_power * self.direction)
            msleep(10)
        if should_stop:
            m.deactivate_motors()


    def lfollow_choppy(self, time, should_stop=True):
        sec = seconds() + time / 1000.0
        while seconds() < sec:
            if black_left():
                mav(c.RIGHT_MOTOR, 0)
                m.av(c.LEFT_MOTOR, c.BASE_LM_POWER)
            elif isLeftOnWhite():
                mav(c.LEFT_MOTOR, 0)
                m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER)
            msleep(c.LFOLLOW_REFRESH_RATE)
        if should_stop:
            m.deactivate_motors()
        