# -*- coding: utf-8 -*-

import os, tempfile, shutil

class OneOffFileStorage:
    """ Stores values in separate files (one value per file). Recreates files on every save. Made for flash drives (SDcards etc) """

    def __init__(self, dir_name):
        self.dir_name = dir_name


    def _filename(self, base_filename, extension):
        return os.path.join(self.dir_name, base_filename + "." + extension)


    def _load(self, name, extension, fallback=None, wrapper=None):
        if wrapper is None:
            wrapper = lambda x: x
        try:
            with open(self._filename(name, extension)) as f:
                return wrapper(f.readline().strip())
        except IOError:
            return fallback


    def _save(self, name, raw_value, extension):
        tmp = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        tmp.write(raw_value)
        tmp.close()
        shutil.move(tmp.name, self._filename(name, extension))


    def get(self, name, fallback=''):
        return self._load(name, 'string', fallback='')


    def get_int(self, name, fallback=None):
        return self._load(name, 'int', wrapper=int, fallback=fallback)


    def set(self, name, value):
        self._save(name, value, 'string')


    def set_int(self, name, value):
        self._save(name, str(value) + "\n", 'int')


