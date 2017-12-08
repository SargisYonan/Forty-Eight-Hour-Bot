import wiringpi
import framework

reset_switch = 22 # GPIO pin 22
last_state = 0

def switch_init():
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(reset_switch, 0) # set reset seitch to an output
    last_state = wiringpi.digitalRead(reset_switch)

def switch_event_checker():
    params = wiringpi.digitalRead(reset_switch)
    if ((params != last_state) and (params == 1)):
    	post_event = framework.Event('RESET_HSM', params)
    	framework.framework_post_event(post_event)

    elif ((params != last_state) and (params == 0)):
    	post_event = framework.Event('STOP_HSM', params)
    	framework.framework_post_event(post_event)

    else:
    	return

