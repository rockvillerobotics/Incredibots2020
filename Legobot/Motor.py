from wombat import *
import constants as c

class Motor:
    all_motors = []
    
    # Consider these "private variables"
    def __init__(self, port, base_power, direction=1):
        self.port = port
        self.current_power = 0
        self.base_power = base_power
        self.half_power = base_power / 2
        self.full_power = base_power
        self.direction = direction
        Motor.all_motors.append(port)
        


    # This is relative to a forward direction. Current power 
    def get_power(self):
        return self.current_power


    def set_power(self, power):
        if power > 1450:
            power = 1450
        elif power < -1450:
            power = -1450
        mav(self.port, int(self.direction * power))
        self.current_power = int(self.direction * power)

    
    def set_reference_powers(self, new_reference_power):
        self.base_power = new_reference_power
        self.full_power = new_reference_power
        self.half_power = new_reference_power / 2


    # This is relative to a forward direction.
    def get_tics(self):
        return gmpc(self.port) * self.direction


    def clear_tics(self):
        cmpc(self.port)
    
    
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
        self.set_power(desired_power)  # Ensures actual desired value is reached

    # TODO add decelleration
    def stop(self):
        self.set_power(0)


    @print_function_name_with_arrows
    def forwards_until(self, boolean_function, *, time=c.SAFETY_TIME, should_stop=True):
        # Left motor goes forwards until right tophat senses black
        self.accelerate_to(self.base_power)
        sec = seconds() + time / 1000.0
        while seconds() < sec and not(boolean_function()):
            msleep(1)
        if should_stop:
            self.stop()
    
    
    @print_function_name_with_arrows
    def backwards_until(self, boolean_function, *, time=c.SAFETY_TIME, should_stop=True):
        # Left motor goes forwards until right tophat senses black
        self.accelerate_to(-self.base_power)
        sec = seconds() + time / 1000.0
        while seconds() < sec and not(boolean_function()):
            msleep(1)
        if should_stop:
            self.stop()
            
            
    # This function treats the motor like a servo.
    @print_function_name_with_arrows
    def move(self, desired_tic_location, desired_speed):
        if desired_tic_location - self.get_tics() > 0:
            desired_speed = desired_speed
        elif desired_tic_location - self.get_tics() < 0:
            desired_speed = -desired_speed
        else:
            print "Boi you're bad. The desired location and the current location are the same."
        print "Current tic location: " + str(get_motor_tics(c.AMBULANCE_ARM_MOTOR))
        print "Desired tic location: " + str(desired_tic_location)
        sec = seconds() + 2000 / 1000.0
        while seconds() < sec and abs(desired_tic_location - self.get_tics()) > 5:
            speed = (desired_tic_location - self.get_tics()) * 20
            if speed > desired_speed:
                speed = desired_speed
            elif speed < desired_speed:
                speed = desired_speed
            elif speed >= 0 and speed < 11:
                speed = 11
            elif speed < 0 and speed > -11:
                speed = -11
            self.set_power(speed)
            msleep(1)
        self.stop()