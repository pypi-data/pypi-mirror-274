#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'adions025@gmail.com'

import logging
import os
from datetime import datetime
from enum import Enum


class LoggerMinimumLevel(Enum):
    """
        Minimum accepted logger level
    """
    CRITICAL = 0
    DEBUG = 1
    ERROR = 2
    FATAL = 3
    INFO = 4
    WARNING = 5


class Log(object):
    """
        Class for merge logger options
    """

    def __init__(self):
        """
            Basic constructor
        """
        self.__logger = None

    def setting_to_file(self, logger_path: str, logger_file_name: str, minimum_level: LoggerMinimumLevel):
        """
            Method for setting logger configuration and save messages in file.
        """
        try:
            if not os.path.isdir(logger_path):
                os.mkdir(logger_path)
            logging.basicConfig(
                filename='%s/%s_%s.log' % (logger_path, logger_file_name, datetime.today().strftime('%Y%m%d')),
                filemode='a', format='%(asctime)s - [%(levelname)s] -  %(message)s',
                datefmt='%Y/%m/%d %H:%M:%S',
                level=self.__get_level(minimum_level.value))
            logging.getLogger('python')
            logger = logging.getLogger('python')
            logger.setLevel(self.__get_level(minimum_level.value))
            self.__logger = logger
        except Exception:
            self.__logger = None
        return self.__logger

    def setting_to_logstash(self, host: str, port: int, minimum_level: LoggerMinimumLevel):
        """
            Method for setting logger configuration using logstash.
            @host: Ip or Name of Logstash server.
            @port: Logstash Listen Port. Normally is 5959. Review you logstash configuration.
            We can add extra information when send message using dictionaries. Sample:
                extraFields = {'Field1': value1, 'Field2': value2}
                logger.info(msg='Message',extra=extraFields)
        """
        import logstash
        try:
            logger = logging.getLogger('python-logstash')
            logger.setLevel(self.__get_level(minimum_level.value))
            logger.addHandler(logstash.LogstashHandler(host, port, version=1))
            self.__logger = logger
        except Exception:
            self.__logger = None
        return self.__logger

    def __get_level(self, level):
        """
            Private method for select level request by parameter
        """
        levelSelected = None
        if level == LoggerMinimumLevel.CRITICAL.value:
            levelSelected = logging.CRITICAL
        elif level == LoggerMinimumLevel.DEBUG.value:
            levelSelected = logging.DEBUG
        elif level == LoggerMinimumLevel.ERROR.value:
            levelSelected = logging.ERROR
        elif level == LoggerMinimumLevel.FATAL.value:
            levelSelected = logging.FATAL
        elif level == LoggerMinimumLevel.INFO.value:
            levelSelected = logging.INFO
        elif level == LoggerMinimumLevel.WARNING.value:
            levelSelected = logging.WARNING
        else:
            levelSelected = logging.DEBUG
        return levelSelected
