import framework.py
import time
winch_timer = 5 # 5 seconds
servo_wait_timer = 2 # 1 second
class State:
	def __init__(self):
		pass

class TurningOnWinch(State):
	def __init__(self):
		self.name = 'Turning on Winch'
	def run(self, event):
		#turn on motor using stepper motor module
		timer.sleep(winch_timer) #start timer(winch_timer)
		return 'winchtimerexpired'
	def entry(self, event):
		return 0
	def exit(self, event):
		return 0

class UnloadingBall(State):
	def __init__(self):
		self.name = 'Unloading Ball'
	def run(self, event):
		#turn on servo using stepper motor module
		timer.sleep(servo_wait_timer)#start timer(servo_wait_timer)
		return 'ServoDone'
	def entry(self, event):
		return 0
	def exit(self, event):
		return 0

class RetractWinch(State):
	def __init__(self):
		self.name = 'Retracting Winch'
	def run(self, event):
		#turn on motor in reverse direction using stepper motor module
		timer.sleep(winch_timer) #start timer(winch_timer)
		return 'winchtimerexpired'
	def entry(self, event):
		return 0
	def exit(self, event):
		return 0
class BallShootingState(State):
	def __init__(self):
		self.name = 'BallShootingState'

		self.turningonwinchstate = TurningOnWinch()
		self.unloadingballstate = UnloadingBall()		
		self.retractwinchstate= RetractWinch()
		
		self.initial_state = self.state_one
		self.current_state = self.initial_state
		self.next_state = self.initial_state

	def run(self, event):
		if (self.current_state == self.turningonwinchstate):
			ret = self.turningonwinchstate,run(event)
			#turn on winch timer
			if (ret == 'winchtimerexpired'): # expired timer need to make timer function
				self.next_state = self.state_two

		elif (self.current_state == self.unloadingballstate):
			ret = self.unloadingballstate.run(event) 
			if ret == 'ServoDone':
				self.next_state = self.retractwinchstate

		elif (self.current_state == self.retractwinchstate):
			ret = self.retractwinchstate.run(event)
			if ret == 'winchtimerexpired':
				self.next_state = self.turningonwinchstate
			elif ret == 'ServoDone' :
				self.next_state = self.unloadingballstate
			return 0

		# if a transition has occured
		if self.next_state != self.current_state:
			self.current_state.exit()
			self.current_state = self.next_state
			self.current_state.entry()

	def entry(self):
		self.current_state = self.initial_state
		self.next_state = self.initial_state
		return 1

	def exit(self):
		# stop actuating
		return 0

	
AFSM = StateA()

# HSM - F
#      |_ A
#         |_ 1
#         |_ 2
#         |_ 3
#      |_ B
#      |_ C

## Step 1. Create bottom most states first (1, 2, 3)


