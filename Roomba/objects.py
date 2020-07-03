import Cliff
import Depth
import Servo
import Limit
import constants as c

#---------------Servo Objects-------------------
# Parameters: port, starting_value

arm_servo = Servo(3, 1024)
claw_servo = Servo(1, 1024)

#---------------Cliff Objects-------------------
# Parameters: value command, side

lcliff = Cliff(get_create_lcliff_amt, side=c.LEFT)
rcliff = Cliff(get_create_rcliff_amt, side=c.RIGHT)
lfcliff = Cliff(get_create_lfcliff_amt, side=c.LEFT)
rfcliff = Cliff(get_create_rfcliff_amtm, side=c.RIGHT)

#---------------Tophat Objects------------------
# Parameters: port, location, tophat_type
# Locations are left, right, front, and back. These help make lfollows
#   work the way you want. 


#---------------Depth Objects--------------------
# Parameters: port, value midpoint

left_depth = Depth(0, 1300)

#---------------Limit Switch Objects-------------
# Parameters: port

left_limit = Limit(0)
