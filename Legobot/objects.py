import Servo
import Motor
import Tophat

left_motor = Motor(3)
right_motor = Motor(2)

arm_servo = Servo(1)
claw_servo = Servo(4)


import objects as o

o.arm_servo.move(2000)
print(o.arm_servo.get_current_pos)
print(o.arm_servo.get_current_pos)

Servo.get_current_pos(arm_servo)
Servo.get_current_pos(claw_servo)

arm_servo.get_current_pos()
claw_servo.get_current_pos()

left_motor.get_current_pos()