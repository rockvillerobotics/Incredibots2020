import Cliff
import constants as c

lcliff = Cliff(get_create_lcliff_amt, side=c.LEFT)
rcliff = Cliff(get_create_rcliff_amt, side=c.RIGHT)
lfcliff = Cliff(get_create_lfcliff_amt, side=c.LEFT)
rfcliff = Cliff(get_create_rfcliff_amtm, side=c.RIGHT)