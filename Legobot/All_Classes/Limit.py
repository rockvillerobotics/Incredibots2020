import ctypes
KIPR=ctypes.CDLL("/usr/lib/libkipr.so")

class Limit:
    
    def __init__(self, port):
        self.port = port

    def get_value(self):
        return KIPR.digital(self.port)

    def is_pressed(self):
        return self.get_value() == 1

    def is_unpressed(self):
        return self.get_value() == 0
