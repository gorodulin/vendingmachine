# -*- coding: utf-8 -*-

import signal
import logging.config
import threading
from vendingmachine.machine import Machine

logging.config.fileConfig('/app/logger.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('START')
    machine = Machine()
    signal.signal(signal.SIGINT, machine.sig_handler) # Register SIGINT handler

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

