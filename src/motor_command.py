 
#control motors from command line
"""
example:  python motor_command.py 1 -50

"""

import motors
import sys

mc = motors.MotorController()
print("modifying motor", sys.argv[1], "to speed", sys.argv[2],"...")

mc.set_motor_speed( int(sys.argv[1]) , int( sys.argv[2]))

"""
 ______________________________________
/ You'd like to do it instantaneously, \
\ but that's too slow.                 /
 --------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
"""
