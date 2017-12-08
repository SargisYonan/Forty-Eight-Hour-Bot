import hsm

events_list = []
task_list = []

class Event:
    def __init__(self, name, params):
        self.name = name
        self.params = params

def framework_post_event(event) : #function to add event strings to a list
    events_list.append(event) 

## used by the Task Obj instance creator
def framework_add_task(task): #function to add event checker strings to a list
    task_list.append(task)

def start_framework(): #for loop through the task_list run through event list f
    while(True):
        for task in task_list: 
            if framework_debug:
                print 'Running Task: ' + task.name + '\n'
            task.task() 

            # run all posted events from the last check if they exist
            for event in events_list:
                if framework_debug:
                    print ('Entering event')

                hsm.hsm(event)
                events_list.remove(event)


class Task():
    def __init__(self, name, task_ptr):
        self.name = name
        self.task_ptr = task_ptr

        framework_add_task(self)
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


