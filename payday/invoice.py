# -*- coding: utf-8 -*-

'''
Created on Oct 3, 2014

@author: pk
'''

import os

from payday import utils
from payday import errors


class Invoice(object):

    def __init__(self, path, client):
        self.basedir = os.path.dirname(path)
        self.client = client
        self.path = path
        self.invoice = self._load_invoice_from_file(path)

    def _load_invoice_from_file(self, path):
        data = utils.parse_yaml_from_file(path)
        if type(data) != dict:
            raise errors.PaydayError(
                "parse error: invoice must be formatted as a YAML dict, got {} ({})".format(type(data), path))
        if 'id' not in data:
            raise errors.PaydayError(
                "validation error: invoice must have an 'id' attribute ({})".format(path))
        if type(data['id']) != str:
            raise errors.PaydayError(
                "validation error: invoice must have a str 'id' attribute ({})".format(path))
        return data

    def id(self):
        return self.invoice['id']

    def __str__(self):
        return "%s %s %s" % (self.invoice['id'], self.client, self.path)
