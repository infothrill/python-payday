# -*- coding: utf-8 -*-

"""Client code."""

import os
import logging
import fnmatch
import re
from itertools import chain

from . import utils
from . import errors
from .invoice import Invoice

logger = logging.getLogger(__name__)


class Client(object):

    def __init__(self, client):
        self.basedir = os.path.dirname(client)
        self.filename = client
        self.shortname = os.path.basename(os.path.dirname(client))
        self.client = self._load_client_from_file(client)
        self.invoices = self._load_invoices()

    def _load_client_from_file(self, path):
        client_data = utils.parse_yaml_from_file(path)
        if type(client_data) != dict:
            raise errors.PaydayError(
                "parse error: clients must be formatted as a YAML list, got %s" % type(client_data))
        if 'name' not in client_data:
            raise errors.PaydayError("clients must have a 'name' attribute!")
        return client_data

    def _load_invoices(self):
        invoices = []
        invoicedir = os.path.join(self.basedir, "invoices")
        if os.path.isdir(invoicedir):
            for apath in os.listdir(invoicedir):
                invoicepath = os.path.join(invoicedir, apath)
                if apath.endswith(".yml") and os.path.isfile(invoicepath):
                    invoices.append(Invoice(invoicepath, self))
        else:
            logger.debug("No invoices in %s", self.basedir)
        return invoices

    def invoice(self, n):
        matching = [x for x in self.invoices if x.invoice['id'] == n]
        if len(matching) > 1:
            raise errors.PaydayError(
                "Multiple invoices with number {} found".format(n))
        elif len(matching) == 1:
            return matching[0]
        else:
            raise errors.PaydayError(
                "No invoice with number {} found".format(n))

    def __str__(self):
        return "%s" % (self.client.get('name'))


def find_clients(path):
    includes = ['meta.yml', 'meta.yaml']
    includes = r'|'.join([fnmatch.translate(x) for x in includes])
    for root, _, files in os.walk(path):
        files = [f for f in files if re.match(includes, f)]
        if len(files):
            for filename in files:
                absname = os.path.join(root, filename)
                logger.debug("Found client file %s, loading...", absname)
                yield Client(absname)


def find_invoices(path="."):
    """Generates `payday.invoice` objects from path.

    :param path: path to look for invoices
    """
    return chain.from_iterable(client.invoices for client in find_clients(path))


def find_invoice(invoice_id, path="."):
    for invoice in find_invoices(path):
        if invoice.id() == invoice_id:
            return invoice
    raise ValueError("The given invoice '%s' could not be found." % invoice_id)
