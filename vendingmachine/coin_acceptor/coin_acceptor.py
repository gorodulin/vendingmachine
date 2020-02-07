# -*- coding: utf-8 -*-

import logging
import struct
import time
from bitstring import BitArray
from cctalk import Message
from cctalk.coinacceptor import CoinAcceptor

logger = logging.getLogger(__name__)

ACCEPTABLE_COINS = {
    'RU1K0A': 10,  # pos 7 (inhabit err code 134)
    'RU050C': 0.5,  # pos 8 (inhabit err code 135)
    'RU050B': 0.5,  # pos 9 (inhabit err code 136)
    'RU100A': 1,  # pos 10 (inhabit err code 137)
    'RU100B': 1,  # pos 11 (inhabit err code 138)
    'RU200B': 2,  # pos 12 (inhabit err code 139)
    'RU200A': 2,  # pos 13 (inhabit err code 140)
    'RU500B': 5,  # pos 14 (inhabit err code 141)
    'RU500A': 5,  # pos 15 (inhabit err code 142)
    'RU1K0B': 10,  # pos 16 (inhabit err code 143)
}


class MyCoinAcceptor(CoinAcceptor):

    def __init__(self, iface, insert_cb=None, error_cb=None):
        super(MyCoinAcceptor, self).__init__(iface)
        self._insert_callback = insert_cb
        self._error_callback = error_cb


    def onInitCompleted(self):
        logger.info("CA Manufacturer:\t\t{}".format(self.manufacturer))
        logger.info("Equipment Category:\t{}".format(self.equipment_category))
        logger.info("Product Code:\t\t{}".format(self.product_code))
        self.setAcceptableCoins(ACCEPTABLE_COINS)
        self.setInhibitOff()


    def onCoinAccept(self, coin):
        coin_value = ACCEPTABLE_COINS[coin._Coin__id]
        self._insert_callback(coin_value)


    def onError(self, error_code):
        self._error_callback(error_code)


    def setAcceptableCoins(self, acceptable_coins_dict):
        msg = Message(src=1, dst=self.addr, header=Message.HEADER_REQ_COINID)
        bits = ''
        for x in range(1, 17):
            msg.data = struct.pack('B', x)
            response = self.iface.send(msg)
            slug = response.data.decode('ascii')
            bits += "1" if (slug in acceptable_coins_dict) else "0"
        bitarray = BitArray('0b' + bits)
        msg = Message(src=1, dst=self.addr, header=Message.HEADER_MOD_INHIBIT, data=bitarray.bytes)
        response = self.iface.send(msg)


    def setInhibitOff(self):
        """ Set inhibit off (all coins) """
        msg = Message(src=1, dst=self.addr, header=Message.HEADER_MOD_MASTER_INHIBIT, data=b'\x01')
        #self.iface.ser.cancel_read()
        self.pause_polling = True
        time.sleep(0.2)
        self.iface.send(msg)
        self.pause_polling = False
        #logger.debug('[evt #{}] master inhibit turned ON'.format(self.events))


    def setInhibitOn(self):
        """ Set inhibit on (all coins) """
        msg = Message(src=1, dst=self.addr, header=Message.HEADER_MOD_MASTER_INHIBIT, data=b'\x00')
        self.pause_polling = True
        time.sleep(0.2)
        self.iface.send(msg)
        self.pause_polling = False


    def stop(self):
        self.iface._Interface__loop = False
        #self.iface._Interface__devices = []

