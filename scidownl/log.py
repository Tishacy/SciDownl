# -*- coding: utf-8 -*-
import sys
from threading import RLock

from loguru import logger

from .config import get_config

configs = get_config()


class LoggerLoader:
    _init_status = False
    _lock = RLock()
    _loggers = {}

    def _log_init(self):
        """Initialize loggings."""
        # Load log configs
        log_level = configs['log']['console_log_level']
        log_format = configs['log']['console_log_format']

        logger.remove()
        loggers = {}
        # Add default logger
        default_logger_name = 'default'
        logger.add(sys.stderr,
                   level=log_level,
                   filter=self._make_filter(name=default_logger_name),
                   format=log_format)
        default_logger = logger.bind(name=default_logger_name)
        loggers[default_logger_name] = default_logger
        default_logger.debug("Registered the default logger")
        return loggers

    @staticmethod
    def _make_filter(name):
        return lambda record: record["extra"].get("name") == name

    @staticmethod
    def load(logger_name: str):
        """Returns the loguru.Logger based on logger name.

        :param logger_name: Logger name.
        :return: a loguru.Logger.
        """
        if not LoggerLoader._init_status:
            with LoggerLoader._lock:
                if not LoggerLoader._init_status:
                    LoggerLoader._loggers = LoggerLoader()._log_init()
                    LoggerLoader._init_status = True
        return LoggerLoader._loggers.get(logger_name)


def get_logger(name=None):
    name = name or 'default'
    return LoggerLoader.load(name)
