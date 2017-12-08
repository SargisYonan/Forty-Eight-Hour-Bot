import framework
import hole_finding_state

STATE_COMPLETE = 1
STATE_NOT_COMPLETE = 0

class State:
    def __init__(self):
        pass

class IdlingState(State):
    def __init__(self):
        self.name = 'Idling'

    def run(self, event):
        if (event.name == 'RESET_HSM'):
            return STATE_COMPLETE
        else:
            return STATE_NOT_COMPLETE

    def entry(self, event):
        all_motors_stop()
        return

    def exit(self, event):
        return

class HoleFindingState(State):
    def __init__(self):
        self.name = 'Hole Finding State'

        self.rotating_state = hole_finding_state.RotatingState()
        self.driving_state = hole_finding_state.DrivingState()
        self.aligning_state= hole_finding_state.AligningState()

        self.initial_state = self.rotating_state
        self.current_state = self.initial_state
        self.next_state = self.initial_state

    def run(self, event):
        if (self.current_state == self.rotating_state):
            ret = self.rotating_state.run(event)
            if ret == hole_finding_state.HOLE_FOUND:
                self.next_state = self.driving_state
                
        elif (self.current_state == self.driving_state):
            ret = self.driving_state.run(event)
            if ret == hole_finding_state.HOLE_LOST:
                self.next_state = self.rotating_state
            elif ret == hole_finding_state.HOLE_CLOSE:
                self.next_state = self.aligning_state

        elif (self.current_state == self.aligning_state):
            ret = self.aligning_state.run(event)
            if ret == hole_finding_state.BALL_SHOT:
                self.next_state = self.rotating_state

        # if a transition has occured
        if self.next_state != self.current_state:
            self.current_state.exit(event)
            self.current_state = self.next_state
            self.current_state.entry(event)

    def entry(self, event):
        self.current_state = self.initial_state
        self.next_state = self.initial_state
        return

    def exit(self, event):
        motors_stop_all()
        return

class BallShootingState(State):
    def __init__(self):
        self.name = 'Ball Shooting State'

    def run(self, event):
        return
    def entry(self, event):
        return
    def exit(self, event):
        return

class GeorgeHSM(State):
    def __init__(self):
        self.name = 'George HSM'

        self.idling_state = IdlingState()
        self.hole_finding_state = HoleFindingState()
        self.ball_shooting_state= BallShootingState()

        self.initial_state = self.idling_state
        self.current_state = self.initial_state
        self.next_state = self.initial_state

    def run(self, event):
        if (event.name == 'STOP_HSM') and (self.current_state != self.idling_state):
            self.next_state = self.idling_state

        elif (self.current_state == self.idling_state):
            ret = self.idling_state.run(event)
            if ret == STATE_COMPLETE:
                self.next_state = self.hole_finding_state

        elif (self.current_state == self.hole_finding_state):
            ret = self.hole_finding_state.run(event)
            if ret == STATE_COMPLETE:
                self.next_state = self.ball_shooting_state

        elif (self.current_state == self.ball_shooting_state):
            ret = self.ball_shooting_state.run(event)
            if ret == STATE_COMPLETE:
                self.next_state = self.hole_scanning_state

        # if a transition has occured
        if self.next_state != self.current_state:
            self.current_state.exit(event)
            self.current_state = self.next_state
            self.current_state.entry(event)

    def entry(self, event):
        self.current_state = self.initial_state
        self.next_state = self.initial_state
        return

    def exit(self):
        # stop actuating
        return

george_hsm = GeorgeHSM()
def hsm(event):
    george_hsm.run(event)
