events_list = []
task_list = []

def framework_post_event(event):
	events_list.append(event)

## used by the Task Obj instance creator
def framework_add_event_checker(task):
	task_list.append(task)

def start_framework():
	while(True):
		for task in task_list:
			print 'Running Task: ' + task.name + '\n'
			task.run_task()

			# run all posted events from the last check if they exist
			for event in events_list:
				event()
				events_list.remove(event)


class Task():
	def __init__(self, name, task_ptr):
		self.name = name
		self.task_ptr = task_ptr

		framework_add_event_checker(self)

	def print_my_name(self):
		print self.name

	def run_task(self):
		self.task_ptr()
		
'''
def hole_event():
	print 'shoot ball'

def check_tape():
	print 'tape checking'

def check_hole():
	print 'hole checked'
	framework_post_event(hole_event)

tape_chk = Task('Tape Checker', check_tape)
hole_chk = Task('Hole Checker', check_hole)

start_framework()

'''


