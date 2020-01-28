# -*- coding: utf-8 -*-

import threading
from time import sleep

class Watchdog(threading.Thread):
    """ Monitors `error_probe_cb` callback result every `interval` seconds..
        If result changes to True, runs on_error_cb callback, otherwise runs on_recover_cb.
    """

    _loop = True

    def __init__(self, error_probe_cb=None, on_error_cb=None, on_recover_cb=None, interval=3):
        threading.Thread.__init__(self)
        self.name = "Watchdog"
        self.callback_for = { True: on_error_cb, False: on_recover_cb }
        self.error_probe_cb = error_probe_cb
        self.interval = interval
        self.healthy = None


    @classmethod
    def stop(cls):
        cls._loop = False


    def run(self):
        """ Continuous self-checking """
        last = self.error_probe_cb()
        while self.__class__._loop:
            sleep(self.interval)
            state = self.error_probe_cb()
            if last == state:
                continue
            self.callback_for[state]()
            last = state
