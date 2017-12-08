import switch
import framework
import hole_service

## place all event checker framwork code here
switch_checker = framework.Task('Switch Checker', switch.switch_event_checker)
hole_checker = framework.Task('Hole Checker', switch.hole_event_checker)

## place all event checker system level init calls here
switch.switch_init()
hole_service.init()

## must start the framework
framework.start_framework()