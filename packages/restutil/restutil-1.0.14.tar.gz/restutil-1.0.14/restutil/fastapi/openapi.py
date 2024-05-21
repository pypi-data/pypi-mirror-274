#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'adions025@gmail.com'

HTTP_METHODS = ["post", "get", "put", "delete"]


def custom_openapi(openapi_schema: dict):
    def wrapper():
        for method in openapi_schema["paths"]:
            for m in HTTP_METHODS:
                try:
                    del openapi_schema["paths"][method][m]["responses"]["422"]
                except KeyError:
                    pass
        for schema in list(openapi_schema["components"]["schemas"]):
            if schema in ["HTTPValidationError", "ValidationError"]:
                del openapi_schema["components"]["schemas"][schema]
        return openapi_schema
    return wrapper
