# -*- coding: utf-8 -*-

'''
Created on Oct 3, 2014

@author: pk
'''


class PaydayError(Exception):
    ''' The base exception from which all others should subclass '''

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
