class State:
	def __init__(self):
		pass

class StateOne(State):
	def __init__(self):
		self.name = 'State One'

	def run(self, event):
		return
	def entry(self, event):
		return
	def exit(self, event):
		return

class StateTwo(State):
	def __init__(self):
		self.name = 'State Two'

	def run(self, event):
		return
	def entry(self, event):
		return
	def exit(self, event):
		return

class StateThree(State):
	def __init__(self):
		self.name = 'State Three'

	def run(self, event):
		return
	def entry(self, event):
		return
	def exit(self, event):
		return


class StateA(State):
	def __init__(self):
		self.name = 'State A'

		self.state_one = StateThree()
		self.state_two = StateThree()		
		self.state_three = StateThree()
		
		self.initial_state = self.state_one
		self.current_state = self.initial_state
		self.next_state = self.initial_state

	def run(self, event):
		if (self.current_state == self.state_one):
			ret = self.state_one,run(event)
			if (ret == 'made_up_signal_1'):
				self.next_state = self.state_two

		elif (self.current_state == self.state_two):
			ret = self.state_two.run(event) 
			if ret == 'made_up_signal_2':
				self.next_state = self.state_three

		elif (self.current_state == self.state_three):
			ret = self.state_three.run(event)
			if ret == 'made_up_signal_3':
				self.next_state = self.state_one
			elif ret == 'something_else':
				self.next_state = self.state_two

		# if a transition has occured
		if self.next_state != self.current_state:
			self.current_state.exit()
			self.current_state = self.next_state
			self.current_state.entry()

	def entry(self):
		self.current_state = self.initial_state
		self.next_state = self.initial_state
		return

	def exit(self):
		# stop actuating
		return

	
AFSM = StateA()

# HSM - F
#      |_ A
#         |_ 1
#         |_ 2
#         |_ 3
#      |_ B
#      |_ C

## Step 1. Create bottom most states first (1, 2, 3)


