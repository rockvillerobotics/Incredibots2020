from wombat import *

class Servo:
    # A constructor
    def __init__(self, port):
        self.name = name
        self.age = age
        self.current_pos = 1024

    # ~~~~ Getters ~~~~
    # Note: Getters and setters are the proper way to interface with an object's data.

    def get_current_pos(self):
        return self.current_pos

    # ~~~~ Instance methods ~~~~