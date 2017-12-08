#Motor drivers for the pi:
#maxL is doing the first pass, he'll assume we're using python 3,
#but 2 should work as well...

# motor one is left/blue
# motor four is right/green
# motor two is butt/white
# motor four is arm

left_wheel = 1
right_wheel = 4
back_wheel = 2
arm = 3

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

    clockwise_speed = 10
    def rotate_clockwise():
        self.set_motor_speed(left_wheel, clockwise_speed)
        self.set_motor_speed(right_wheel, clockwise_speed)
        self.set_motor_speed(back_wheel, clockwise_speed)

    drive_forward_speed = 20
    def drive_forward():
        self.set_motor_speed(left_wheel, drive_forward_speed)
        self.set_motor_speed(right_wheel, drive_forward_speed)
        self.set_motor_speed(back_wheel, 0)

    def motors_extend_arm():
        self.set_motor_speed(arm, 30)
        time.sleep(1)
        self.set_motor_speed(arm, 0)

    def release_ball():

    def move_left():
        self.set_motor_speed(left_wheel, -1 * drive_forward_speed)
        self.set_motor_speed(right_wheel, drive_forward_speed)
        self.set_motor_speed(back_wheel, -1 * drive_forward_speed)

    def move_right():
        self.set_motor_speed(left_wheel, drive_forward_speed)
        self.set_motor_speed(right_wheel, -1 * drive_forward_speed)
        self.set_motor_speed(back_wheel, drive_forward_speed)

    def right_angle_cw():
        rotate_clockwise()
        time.sleep(2)
        stop_motors()

    def retract_arm():
        self.set_motor_speed(arm, -30)
        time.sleep(1)
        self.set_motor_speed(arm, 0)

    def stop_motors():
        self.all_motors_stop()

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
