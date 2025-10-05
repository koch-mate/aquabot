import RPi.GPIO as GPIO
import time

from conf import pins
from lib import common

from transitions import Machine

# setup GPIO
#

GPIO.setmode(GPIO.BCM)

for s in pins.SWITCHES:
    GPIO.setup(s, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for l in pins.LEDS:
    GPIO.setup(l, GPIO.OUT)
    GPIO.output(l, GPIO.LOW)

try:
    while True:
        time.sleep(0.02)
        GPIO.output(pins.LEF, GPIO.input(pins.SWB))
        GPIO.output(pins.LER, GPIO.input(pins.SWTCCW))

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()


class Robot:
    states = ["off", "boot", "calibrate", "idle", "move"]

    def __init__(self, name):
        self.name = name
        self.machine = Machine(model=self, states=Robot.states, initial="off")

        self.machine.add_transition("start", "off", "boot")
        self.machine.add_transition("bootReady", "boot", "calibrate")
        self.machine.add_transition("calibrateOk", "calibrate", "idle")
        self.machine.add_transition("calibrateOk", "calibrate", "off")
        self.machine.add_transition("shutdown", "*", "off")

    def run(self):
        pass


robot = Robot("aquabot")
