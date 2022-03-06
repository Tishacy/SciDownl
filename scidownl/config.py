# -*- coding: utf-8 -*-
import os
import sys
import configparser
from threading import RLock


class GlobalConfig(object):
    _init_status = False
    _lock = RLock()
    _configs = None
    package_dir = os.path.dirname(__file__)
    config_fpath = os.path.abspath(os.path.join(package_dir, 'config/global.ini'))

    def _config_init(self):
        # Check if config file exists.
        if not os.path.isfile(self.config_fpath):
            print("Config file not found: %s" % self.config_fpath)
            sys.exit(2)

        # Read configs.
        configs = configparser.ConfigParser()
        configs.read(self.config_fpath)
        return configs

    @staticmethod
    def get_config():
        if not GlobalConfig._init_status:
            with GlobalConfig._lock:
                if not GlobalConfig._init_status:
                    GlobalConfig._configs = GlobalConfig()._config_init()
                    GlobalConfig._init_status = True
        return GlobalConfig._configs


def get_config():
    return GlobalConfig.get_config()
