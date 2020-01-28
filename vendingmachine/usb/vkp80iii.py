# -*- coding: utf-8 -*-

import usb.core
import usb.util

class Printer:

    INTERFACE_CLASS = 7

    def __init__(self, vendor, product, ep_in_addr=0x81, ep_out_addr=0x02, timeout=1):
        self._vendor = vendor
        self._product = product
        self._ep_in_addr = ep_in_addr
        self._ep_out_addr = ep_out_addr
        self.timeout = timeout
        self._open()


    def _open(self):
        self.dev = usb.core.find(idVendor=self._vendor, idProduct=self._product)
        if self.dev is None:
            raise ValueError('Device not found')
        cfg = self.dev.get_active_configuration()
        intf = usb.util.find_descriptor(cfg, bInterfaceClass=Printer.INTERFACE_CLASS)
        if self.dev.is_kernel_driver_active(intf.bInterfaceNumber):
            self.dev.detach_kernel_driver(0)
        self._ep_in  = usb.util.find_descriptor(intf, bEndpointAddress=self._ep_in_addr)
        self._ep_out = usb.util.find_descriptor(intf, bEndpointAddress=self._ep_out_addr)


    def raw(self, msg):
        self.dev.write(self._ep_out, msg, self.timeout)


    def read(self):
        """ Read data buffer and returns it to the caller """
        return self.dev.read(self._ep_in, 16)


    def close(self):
        """ Release USB interface """
        if self.dev:
            usb.util.dispose_resources(self.dev)
        self.dev = None


ESC = b'\x1b'
FS  = b'\x1c'
GS  = b'\x1d'

import enum

from itertools import chain

class VKP80III(Printer):

    STATUSES = {
        'warning': {
            'NOTCH_FOUND': (2, 7),
            },
        'recoverable_errors': {
            'COMMAND_ERR': (4, 5),
            'HEAD_TEMPERATURE_ERR': (4, 0),
            'PSU_VOLTAGE_ERR': (4, 3),
            },
        'unrecoverable_errors': {
            'COVER_OPENED': (3, 0),
            'CUTTER_ERR': (5, 0),
            'EEPROM_ERR': (5, 3),
            'NO_PAPER': (2, 0),
            'PAPER_JAM': (4, 6),
            'RAM_ERR': (5, 2),
            'EMITTER_ERR': (5, 7),
            },
        }

    def reset(self):
        self.raw(ESC + b'\x40')


    def align_at_cut(self):
        """ Align at cut. See page 169 """
        self.raw(GS + b'\xf8') 


    def align_at_print(self):
        """ Align at print """
        self.raw(GS + b'\xf6')


    def get_full_report(self):
        """ Get full report """
        self.raw(b'\x10\x04\x14')
        raw_report = self.read()
        known = self.__class__.STATUSES
        report = dict((el,[]) for el in known.keys())
        for group, statuses in known.items():
            for key, position in statuses.items():
                byte_no, bit_no = position
                if raw_report[byte_no] & 2**bit_no > 0:
                    report[group].append(key)
        return report


    def has_errors(self):
        report = self.get_full_report()
        return not all(len(v) == 0 for v in report.values())


    def errors(self):
        """ All errors as list (wo sections """
        names = list(chain(*self.get_full_report().values()))
        return names


    def has_recoverable_errors(self):
        return len(self.get_full_report()['recoverable_errors']) > 0


    def has_unrecoverable_errors(self):
        return len(self.get_full_report()['unrecoverable_errors']) > 0


    def present_ticket(self):
        """ Present ticket. See page 114 """
        self.raw(FS + b'\x50\x08\x01\x45\xff')


    def cut_at_black_mark(self):
        #self.reset()
        #self.align_at_print()
        self.raw(ESC + b'\x64\x04')
        #self.align_at_cut()
        self.present_ticket()

