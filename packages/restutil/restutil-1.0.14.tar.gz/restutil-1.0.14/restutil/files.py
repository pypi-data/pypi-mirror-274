#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'adions025@gmail.com'

from restutil.decorators import Decorest
from restutil.result import ResData
from restutil.operations import ResOperationType as resType
import os


class FS(object):
    """
        Class with common File System methods/functions
    """

    deco = Decorest()

    def __init__(self):
        """
            Basic constructor
        """
        pass

    @deco.try_log
    def create_dir(self, path: str, name: str, exist: bool = True) -> ResData:
        result: ResData = ResData()
        if name and os.path.exists(path):
            os.makedirs(f'{path}/{name}', exist_ok=exist)
            result.content = os.path.join(path, name)
            result.add_result(message="ok", res_type=resType.SUCCESS)
        else:
            result.content = None
            result.add_result(message="Check name||path ", res_type=resType.WARNING)
        return result
