#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
import subprocess
import sys

SWITCH_PIN  = 26
GPIO.setmode(GPIO.BCM)     # BCM GPIO numbering
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # set input pin
state = bool(GPIO.input(SWITCH_PIN))
print("Monitoring lightswitch on pin {0}".format(SWITCH_PIN))

def lights(channel):
    global SWITCH_PIN
    global state

    if GPIO.input(SWITCH_PIN): 	# switch pin input is 1
        print "Rising edge detected on {} with val: {}".format(SWITCH_PIN, GPIO.input(SWITCH_PIN))
    else: 			# switch pin input is 0
        print "Falling edge detected on {} with val {}".format(SWITCH_PIN, GPIO.input(SWITCH_PIN))

    if state != bool(GPIO.input(SWITCH_PIN)):		# run script only when pin input changes
        subprocess.call("/usr/local/share/scripts/lights/toggle-lights")
        state = bool(GPIO.input(SWITCH_PIN))


# Run function on state change
GPIO.add_event_detect(SWITCH_PIN, GPIO.BOTH, callback=lights)

# Run until cancelled
try:
    sleep(float('inf')) 
except KeyboardInterrupt:
    print("SIGINT Received\n"+
            "Terminating process")
    sys.exit()

finally:                   
    print("cleaning up GPIO pins")
    GPIO.cleanup()       
