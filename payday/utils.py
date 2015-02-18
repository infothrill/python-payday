# -*- coding: utf-8 -*-

"""Some more generic utility methods."""

import io
import yaml

from . import errors


def parse_yaml_from_file(path):
    try:
        with io.open(path, "r", encoding="utf-8") as f:
            data = f.read()
    except IOError:
        raise errors.PaydayError("Could not read file: %s" % path)
    return yaml.safe_load(data)
