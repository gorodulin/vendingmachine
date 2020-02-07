# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

# @see https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/buttons_and_switches/

class Button:

    def __init__(self, gpio_pin, on_press):
        self.channel = int(gpio_pin)
        self.callback = on_press
        if not GPIO.getmode():
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.IN)#, pull_up_down=GPIO.PUD_DOWN)
        self._enabled = False


    def enable(self):
        if not self._enabled:
            # events can be GPIO.RISING, GPIO.FALLING, or GPIO.BOTH
            GPIO.add_event_detect(self.channel, GPIO.RISING, callback=self.callback, bouncetime=200)
            self._enabled = True


    def disable(self):
        if self._enabled:
            GPIO.remove_event_detect(self.channel)
            self._enabled = False


    def cleanup(self):
        GPIO.cleanup(self.channel)

