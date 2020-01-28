# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

class Led:

    def __init__(self, gpio_pin):
        self.channel = int(gpio_pin)
        if not GPIO.getmode():
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.OUT)


    def on(self):
        GPIO.output(self.channel, GPIO.HIGH)


    def off(self):
        GPIO.output(self.channel, GPIO.LOW)


    def cleanup(self):
        GPIO.cleanup(self.channel)


