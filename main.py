import logging

import RPi.GPIO as GPIO
import time

from gpiozero import LED

from conf import pins
from lib import common

from transitions import Machine

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

logging.info("Aquabot booting")

GPIO.setmode(GPIO.BCM)

logging.info("Setting up switches... ")
for k, v in pins.SWITCHES.items():
    GPIO.setup(v, GPIO.IN, pull_up_down=GPIO.PUD_UP)

logging.info("Setting up switches - READY")

logging.info("Setting up LEDs... ")
LEDS = {}
for l in pins.LEDS.keys():
    LEDS[l] = LED(pins.LEDS[l])
logging.info("Setting up LEDs - READY")

try:
    while True:
        time.sleep(0.2)
        for _, L in LEDS.items():
            L.on()
            time.sleep(0.3)
            L.off()


except KeyboardInterrupt:
    logging.info("GPIO cleanup...")

finally:
    GPIO.cleanup()
    logging.info("Shutting down")


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
