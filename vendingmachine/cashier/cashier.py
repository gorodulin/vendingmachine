# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class Cashier:

    def create_receipt(self, price):
        logger.debug("call cashier.create_receipt({})".format(price))

