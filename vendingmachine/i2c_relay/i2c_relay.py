# -*- coding: utf-8 -*-

import smbus

ON  = 0xFF
OFF = 0x00

class I2cRelay:

    def __init__(self, i2c_bus_id, i2c_device_addr, relay_number):
        self.bus = smbus.SMBus(int(i2c_bus_id))
        self.i2c_device_addr = int(i2c_device_addr)
        self.relay_number = int(relay_number)


    def cleanup(self):
        self.off()


    def on(self):
        self.bus.write_byte_data(self.i2c_device_addr, self.relay_number, ON)


    def off(self):
        self.bus.write_byte_data(self.i2c_device_addr, self.relay_number, OFF)


    def state(self):
        return self.bus.read_byte_data(self.i2c_device_addr, self.relay_number)


    def is_on(self):
        return self.state() == ON


    def is_on(self):
        return self.state() == OFF

