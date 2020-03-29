from wombat import *
from decorators import *
import constants as c
import movement as m

class Depth:
    
    def __init__(self, port, value_midpoint):
        self.value_midpoint = value_midpoint
        self.port = port
    
    
    def get_value(self):
        return analog(self.port)


    def senses_depth(self):
        return self.get_value() > self.value_midpoint
    
    
    def senses_nothing(self):
        return self.get_value() < self.value_midpoint        