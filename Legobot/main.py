#!/usr/bin/python3
import io
import os
import sys
import ctypes
KIPR=ctypes.CDLL("/usr/lib/libkipr.so")
from objects import *
import time
import movement as m
import sensors as s
import utils as u
    
    
def main():
    print("Hello World")
    left.lfollow_choppy(1000)
    KIPR.msleep(1000)
    print ("goodbye")
        

if __name__== "__main__":
    try:
        # Python 3, open as binary, then wrap in a TextIOWrapper with write-through.
        sys.stdout = io.TextIOWrapper(open(sys.stdout.fileno(), 'wb', 0), write_through=True)
        # If flushing on newlines is sufficient, as of 3.7 you can instead just call:
        # sys.stdout.reconfigure(line_buffering=True)
    except TypeError:
        # Python 2
        sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    main()
