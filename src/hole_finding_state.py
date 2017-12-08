import hsm
import framework
import motors
import time
import math

# enum-ish
HOLE_FOUND = 10
HOLE_LOST = 11
HOLE_CLOSE = 12
BALL_SHOT = 13

class State:
    def __init__(self):
        pass

class RotatingState(State):
    def __init__(self):
        self.name = 'Rotating State'

    def run(self, event):
        if (event.name == 'HOLE_DETECTED'):
            return hsm.STATE_COMPLETE     
        else:
            return hsm.STATE_NOT_COMPLETE

    def entry(self, event):
        motors.rotate_clockwise() # make sure this is slow
        return

    def exit(self, event):
        motors.stop_motors()
        return

class DrivingState(State):
    def __init__(self):
        self.name = 'Driving State'

    def run(self, event):
        if (event.name == 'HOLE_LOST'):
            return HOLE_LOST
        elif (event.name == 'HOLE_CLOSE'):
            return HOLE_CLOSE
        else:
            return hsm.STATE_NOT_COMPLETE

    def entry(self, event):
        motors.drive_forward()
        return 

    def exit(self, event):
        motors.stop()
        return

class AligningState(State):
    def __init__(self):
        self.name = 'Aligning State'

    def run(self, event):
        if (event.name == HOLE_RIGHT):
            motors.rotate_clockwise()
        elif (event.name == HOLE_LEFT):
            motors.rotate_counter_clockwise()
        elif (event.name == HOLE_CLOSE):
            motors.drive_forward()
        elif (event.name == HOLE_CENTER):
            motors.stop_motors()
            return hsm.STATE_COMPLETE
        else:
            return hsm.STATE_NOT_COMPLETE

    def entry(self, event):
        return

    def exit(self, event):
        motors.motors_extend_arm()
        motors.release_ball()
        motors.retract_arm()
        motors.stop_motors()
        time.sleep(1)
        motors.back_up()
        motors.right_angle_cw()
        return BALL_SHOT
