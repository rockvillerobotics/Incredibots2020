from wombat import *

class Motor:
    
    # Consider these "private variables"
    def __init__(self, port, base_power, coefficient=1):
        self.port = port
        self.current_power = 0
        self.base_power = base_power
        self.half_power = base_power / 2
        self.full_power = base_power
        self.coefficient = coefficient


    # This is relative to a forward direction. Current power 
    def get_power(self):
        return self.current_power


    def set_power(self, power):
        if power > 1450:
            power = 1450
        elif power < -1450:
            power = -1450
        mav(self.port, int(self.coefficient * power))
        self.current_power = int(self.coefficient * power)
        

    def clear_tics(self):
        cmpc(self.port)


    # This is relative to a forward direction.
    def get_tics(self):
        return gmpc(self.port) * self.coefficient
    
    
    def accelerate_to(self, desired_power):
        if desired_power < 1 and desired_power >= 0:
            desired_power = 1
        elif desired_power > -1 and desired_power < 0:
            desired_power = -1
        intermediate_velocity = self.current_power
        if abs(desired_power - self.current_power) > 600 or self.current_power == 0:
             rev = True
        if rev == True:
            velocity_change = desired_power / 30.0
            while abs(intermediate_velocity - desired_power) > 100:
                set_power(self.port, intermediate_velocity)
                intermediate_velocity += velocity_change
                msleep(1)
        set_power(self.port, desired_power)  # Ensures actual desired value is reached