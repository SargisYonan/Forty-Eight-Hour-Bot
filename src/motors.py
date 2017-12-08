#Motor drivers for the pi:
#maxL is doing the first pass, he'll assume we're using python 3,
#but 2 should work as well...

import sys
sys.path.append('./motors_py3')

from motors_py3.Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

class MotorController:
	def __init__(self):
		self.motor_handler = Raspi_MotorHAT(addr=0x6f)

	def set_motor_speed(self, motor_number, speed):
		""" Set the speed of one of the 4 dc motors.
		The three motors are 1, 2, 3, 4.
		Speed is from -100 to 100."""
		motor = self.motor_handler.getMotor(motor_number)
		
		#first, choose direction:
		if speed > 0:
			motor.run(Raspi_MotorHAT.FORWARD)
		else:
			motor.run(Raspi_MotorHAT.BACKWARD)

		#now, figure out the pwm:
		if abs(speed) > 100:
			raise("Speed must be between -100 and 100!")
		pwm = int(  abs(speed)/100 * 255)
		motor.setSpeed(pwm)
		#motor.run(Raspi_MotorHAT.RELEASE)
		
		return
		
	def all_motors_stop(self):
		for motor in [1, 2, 3 , 4]:
			self.set_motor_speed(motor,0)


if __name__=="__main__":
	import time
	print("initializing motor handler")
	mc = MotorController()


	print("all motors forward!!!")
	for motor in [1, 2, 3, 4]:
		mc.set_motor_speed(motor,100)
	time.sleep(1)
	

	print("all motors backward!!!")
	for motor in [1, 2, 3, 4]:
		mc.set_motor_speed(motor,-100)
	time.sleep(1)

	mc.all_motors_stop()

""" 
________________________________________
/ Q: Why don't Scotsmen ever have coffee \
| the way they like it? A: Well, they    |
| like it with two lumps of sugar. If    |
| they drink                             |
|                                        |
| it at home, they only take one, and if |
| they drink it while                    |
|                                        |
\ visiting, they always take three.      /
 ----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

"""
