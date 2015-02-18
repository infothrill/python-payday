# -*- coding: utf-8 -*-

"""Payday exceptions."""


class PaydayError(Exception):
    ''' The base exception from which all others should subclass '''

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
