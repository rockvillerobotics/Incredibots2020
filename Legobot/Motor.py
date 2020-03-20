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
        return self.current_power * self.coefficient


    def set_power(self, power):
        if power > 1450:
            power = 1450
        elif power < -1450:
            power = -1450
        mav(self.port, self.coefficient * power)
        self.current_power = self.coefficient * power
        

    def clear_tics(self):
        cmpc(self.port)


    # This is relative to a forward direction.
    def get_tics(self):
        return gmpc(self.port) * self.coefficient
    
    
            
    def accelerate_to(self, power):
        if desired_velocity < 1 and desired_velocity >= 0:
            desired_velocity = 1
        elif desired_velocity > -1 and desired_velocity < 0:
            desired_velocity = -1
        intermediate_velocity = get_power()
        if abs(desired_velocity - get_power()) > 600 or get_power() == 0:
             rev = True
        if rev == True:
            velocity_change = desired_velocity / 30.0
            while abs(intermediate_velocity - desired_velocity) > 100:
                mav(motor_port, int(intermediate_velocity))
                if motor_port == c.LEFT_MOTOR:
                    c.CURRENT_LM_POWER = desired_velocity
                elif motor_port == c.RIGHT_MOTOR:
                    c.CURRENT_RM_POWER = desired_velocity
                intermediate_velocity += velocity_change
                msleep(1)
                g.update_gyro()
        mav(motor_port, int(desired_velocity))  # Ensures actual desired value is reached
        if motor_port == c.LEFT_MOTOR:
            c.CURRENT_LM_POWER = desired_velocity
        elif motor_port == c.RIGHT_MOTOR:
            c.CURRENT_RM_POWER = desired_velocity