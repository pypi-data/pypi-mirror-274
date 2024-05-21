#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'adions025@gmail.com'

from copy import deepcopy
from os import name


class Common(object):
    """
        Class with common methods/functions
    """

    def __init__(self):
        """
            Basic constructor
        """
        pass

    def get_slash(self):
        """
            Reference of S.O. returned values '\\' - Windows or '/' - Linux
        """
        if name == 'nt':
            return '\\'
        else:
            return '/'

    def do_extra_logger(self, app_name: str, method_name: str, class_name: str, inherited_from: str, *args, **kwargs):
        """
            Public method used for construct dictionary with extra information for send to logger.
            :param app_name: string
            :param method_name: string
            :param class_name: string
            :param inherited_from: string
            :param args: extra data
            :param kwargs: extra dictionary
        """
        extra = dict()
        extra["AppName"] = app_name
        extra["Class"] = class_name
        extra["Method"] = method_name
        extra["inheritedFrom"] = inherited_from
        if kwargs:
            extra.update(kwargs['kwargs'])
        return extra

    def remove_property(self, target: dict, prop: []) -> dict:
        """
            Method used for remove properties from a dictionary
            :param target: dict. Dictionary over that we can do changes
            :para prop: []. Properties of dictionary that we will remove inside.
        """
        try:
            for p in prop:
                del target[p]
        except Exception:
            pass
        return target

    def object_to_dictionary(self, model: object) -> dict:
        """
        Method used for convert model into dictionary
        :param model: object. Object over that we can do conversion to
        dictionary. Previously we do a copy and convert this copy.
        """
        result: dict = dict()
        try:
            bck_model = deepcopy(model)
            result = bck_model.__dict__
        except Exception:
            pass
        return result

