import Motor
import Servo
import Tophat
import constants as c

#---------------Motor Objects--------------------
# Parameters: port, base value, direction
# Direction is the coefficient to motor speed. It can reverse motors.

left_motor = Motor(2, 900, 1)
right_motor = Motor(3, 900, -1)

#---------------Servo Objects-------------------
# Parameters: port, starting_value

arm_servo = Servo(3, 1024)
claw_servo = Servo(1, 1024)

#---------------Tophat Objects------------------
# Parameters: port, location, tophat_type
# Locations are left, right, front, and back. These help make lfollows
#   work the way you want.

left = Tophat(1, location=(c.LEFT, c.FRONT), tophat_type=c.BIG_TOPHAT)
right = Tophat(2, location=(c.RIGHT, c.FRONT), tophat_type=c.BIG_TOPHAT)
third = Tophat(3, location=(c.LEFT, c.BACK), tophat_type=c.SMALL_TOPHAT)

#---------------Depth Objects--------------------
# Parameters: port, value midpoint


#---------------Limit Switch Objects-------------
# Parameters: port

