import switch
import framework

## place all event checker framwork code here
switch_checker = framework.Task('Switch Checker', switch.switch_event_checker)

## place all event checker system level init calls here
switch.switch_init()

## must start the framework
framework.start_framework()