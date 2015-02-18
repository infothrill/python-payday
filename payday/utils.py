# -*- coding: utf-8 -*-

'''
Created on Oct 3, 2014

@author: pk
'''

import io
import yaml

from payday import errors


def parse_yaml_from_file(path):
    try:
        with io.open(path, "r", encoding="utf-8") as f:
            data = f.read()
    except IOError:
        raise errors.PaydayError("Could not read file: %s" % path)
    return yaml.safe_load(data)
