import wiringpi

reset_switch = 22 # GPIO pin 22

def switch_init():
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(reset_switch, 0) # set reset seitch to an output

def check_switch():
    return wiringpi.digitalRead(reset_switch)
