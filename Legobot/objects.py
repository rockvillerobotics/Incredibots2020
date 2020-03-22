import Motor
import Servo
import Tophat


left_motor = Motor(2, 900, 1)
right_motor = Motor(3, 900, -1)

arm_servo = Servo(3, 1024)
claw_servo = Servo(1, 1024)

left = Tophat(1, location=(c.LEFT, c.FRONT), tophat_type=Type.BIG_TOPHAT)
right = Tophat(2, location=(c.RIGHT, c.FRONT), tophat_type=Type.BIG_TOPHAT)
third = Tophat(3, location=(c.LEFT, c.BACK), tophat_type=Type.SMALL_TOPHAT)