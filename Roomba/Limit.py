from wombat import *
from decorators import *
import constants as c
import movement as m

class Limit:

    def __init__(self, port):
        self.port = port

    def get_value(self):
        return digital(self.port)

    def is_pressed(self):
        return self.get_value() == 1

    def is_unpressed(self):
        return self.get_value() == 0
