# -*- coding: utf-8 -*-

import signal
import threading
from vendingmachine.machine import Machine

if __name__ == '__main__':
    machine = Machine()
    signal.signal(signal.SIGINT, machine.sig_handler) # Register SIGINT handler

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

