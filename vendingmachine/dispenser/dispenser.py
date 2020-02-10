# -*- coding: utf-8 -*-

import logging
from time import sleep
from vendingmachine.config.config import config
from vendingmachine.usb.printer import VKP80III

logger = logging.getLogger(__name__)

class Dispenser:
    """ Device-specific dispenser. Rewrite it if needed """

    def __init__(self, after_eject):
        self._printer = VKP80III(
                vendor=int(config.get('printer','vendor'), 0),
                product=int(config.get('printer','product'), 0))
        self._callback_after_eject = after_eject
        self.init()


    def __getattr__(self, attr):
        """ Delegate unknown methods to printer instance """
        return getattr(self._printer, attr)


    def init(self):
        self._printer.reset()


    def eject(self):
        logger.debug("call dispenser.eject()")
        self._printer.cut_at_black_mark()
        sleep(3)
        self._callback_after_eject()

