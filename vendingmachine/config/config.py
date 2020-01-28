# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser

configfile = os.environ['VENDINGMACHINE_CONFIG_FILE'] # Raises error if not set

config = ConfigParser()
config.read(configfile, encoding='utf-8')
