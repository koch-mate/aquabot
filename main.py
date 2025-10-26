import RPi.GPIO as GPIO
import time

from gpiozero import LED

from conf import pins
from lib import common

from transitions import Machine

GPIO.setmode(GPIO.BCM)

for s in pins.SWITCHES:
    GPIO.setup(s, GPIO.IN, pull_up_down=GPIO.PUD_UP)

LEDS = {}
for l in pins.LEDS.keys():
    LEDS[l] = LED(pins.LEDS[l])
print(LEDS)

try:
    while True:
        time.sleep(0.2)
        for k, v in LEDS.items():
            LEDS[v].on()
            time.sleep(0.3)
            LEDS[v].off()


except KeyboardInterrupt:
    print("Cleaning up GPIO...")

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
