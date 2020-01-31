# -*- coding: utf-8 -*-

import random
from mpyg321.mpyg321 import MPyg321Player
from pkg_resources import resource_listdir, resource_filename

PLAYER = MPyg321Player()

PACKAGE = 'vendingmachine.resources.sounds'

# TODO: get rid of this / switch to enum:
BUTTON_PRESS = 'button_press'
COIN_INSERT = 'coin_insert'
COIN_REJECT = 'coin_reject'
MUSIC = "music"
NOISE = "noise"


def get_random_mp3_file(subpackage):
    """ Example: get_random_mp3_file(COIN_REJECT) """
    mp3s = []
    subpackage = "{}.{}".format(PACKAGE, subpackage)
    for n in resource_listdir(subpackage, ''):
        filename = resource_filename(subpackage, n)
        if filename.endswith('.mp3'):
            mp3s.append(filename)
    return random.choice(mp3s)


def play_random(subpackage):
    PLAYER.play_song(get_random_mp3_file(subpackage))


def stop():
    PLAYER.stop()

