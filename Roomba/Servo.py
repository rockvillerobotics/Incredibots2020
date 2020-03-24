from wombat import *
from decorators import *

class Servo:
    universal_max_pos = 1950
    universal_min_pos = 50
    all_servos = []
    
    def __init__(self, port, starting_pos=1024, max_pos=universal_max_pos, min_pos=universal_min_pos):
        self.port = port
        self.max_pos = max_pos
        self.min_pos = min_pos
        self.starting_pos = starting_pos
        if max_pos > min_pos:
            self.direction = 1
        else:
            self.direction = -1
        Servo.all_servos.append(port)
            

    def get_pos(self):
        return get_servo_position(self.port)


    def set_pos(self, pos):
        if direction == 1:
            if pos > self.max_pos:
                pos = self.max_pos
            elif pos < self.min_pos:
                pos = self.min_pos
        else:
            if pos < self.max_pos:
                pos = self.max_pos
            elif pos > self.min_pos:
                pos = self.min_pos
        set_servo_position(self.port, pos)


    def move(self, desired_pos, tics=3, ms=1):
        # Moves a servo to a given position from its current position. The servo and desired position must be specified.
        # Servo move speed = tics / ms
        # >18 tics is too high
        intermediate_position = get_servo_position(self.port)
        print "Moving servo"
        print get_servo_position(self.port) + " --> " + desired_pos
        print "Speed = " + str(tics) + "/" + str(ms) + " tics per ms"
        if tics > 18:
            print "Tic value is too high\n"
            u.sd()
        while abs(get_servo_position(self.port) - desired_pos) > 10:
            # Tolerance of +/- 10 included to account for servo value skipping
            if (get_servo_position(self.port) - desired_pos) >= 1:
                self.set_pos(self.port, intermediate_position)
                intermediate_position -= tics
            elif (get_servo_position(self.port) - desired_pos) < 1:
                self.set_pos(self.port, intermediate_position)
                intermediate_position += tics
            else:
                break
            msleep(ms)
        self.set_pos(self.port, desired_pos)  # Ensures actual desired value is reached. Should be a minor point change
        msleep(30)
        print "Desired position reached. Curent position is %d" % get_servo_position(self.port)
        print "Completed servo_slow\n"


    @print_function_name
    def move_up(self, tics):
        desired_pos = get_servo_position(self.port) + tics * self.direction
        self.move_servo(desired_pos)


    @print_function_name
    def move_down(self):
        desired_pos = get_servo_position(self.port) - tics * self.direction
        self.move_servo(desired_pos)
        
        
    @print_function_name
    def move_right(self):
        desired_pos = get_servo_position(self.port) + tics * self.direction
        self.move_servo(desired_pos)
        
    
    @print_function_name
    def move_left(self):
        desired_pos = get_servo_position(self.port) - tics * self.direction
        self.move_servo(desired_pos)