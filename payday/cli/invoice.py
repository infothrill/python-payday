# -*- coding: utf-8 -*-

"""Main CLI program."""


import sys
import logging
import os
import time

from .. import __version__
from ..client import find_invoice
from ..render import get_jinja2_to_wkhtmltopdf_render_method, get_jinja_renderer
from .. import utils

VALID_ACTIONS = set(("add", "list", "info", "render"))

DEFAULT_TEMPLATE_VARS = "billing/vars.yml"
DEFAULT_TEMPLATE_BASE_PATH = "billing/templates"


def render_invoice(path, invoice_id, out_fname):
    invoice = find_invoice(invoice_id, path)
    client = invoice.client

    data = utils.parse_yaml_from_file(os.path.join(path, DEFAULT_TEMPLATE_VARS))
    data['client'] = client.client
    data['invoice'] = invoice.invoice

    from ..calc import calc_std_bill
    # TODO: cross check this calculation against the stored bill data
    netsum, nettax, totalsum = calc_std_bill([o['amount'] for o in data['invoice']['objects']], data['invoice']['vat'])
    data['invoice']['sum'] = netsum
    data['invoice']['tax'] = nettax
    data['invoice']['totalsum'] = totalsum

    template_filename = "default.html"
    template_path = os.path.abspath(os.path.join(path, DEFAULT_TEMPLATE_BASE_PATH, "default"))

    # initialize rendering
    pdf_render = get_jinja2_to_wkhtmltopdf_render_method(
        get_jinja_renderer(template_path), out_fname)

    # render right away
    pdf_render(template_filename, data)

    do_watchdog = False
    if do_watchdog:
        from ..watchdog import TemplateModifiedHandler, Observer
        # for debugging, install a watchdog:
        event_handler = TemplateModifiedHandler(template_path,
                                                template_filename, data, pdf_render)
        observer = Observer()
        observer.schedule(event_handler, template_path)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


def get_action(args):
    "Validate the user supplied action from the args list."
    for i, arg in enumerate(args):
        if arg in VALID_ACTIONS:
            del args[i]
            return arg
    return None


def build_arg_parser(action):
    import argparse
    usage = "%%(prog)s [%s] [--help] [options] ..." % "|".join(
        VALID_ACTIONS)
    epilog = "\nSee '%s <command> --help' for more information on a specific command.\n\n" % os.path.basename(
        sys.argv[0])
    parser = argparse.ArgumentParser(usage=usage, epilog=epilog)

    # example on how we could extend the parser:
    if action == "list":
        parser.add_argument(
            "path", help="path to work on", nargs="?", default=".")
    elif action == "info":
        parser.add_argument("invoice_id", help="the invoice to show")
        parser.add_argument(
            "path", help="path to work on", nargs="?", default=".")
    elif action == "render":
        parser.add_argument("invoice_id", help="the invoice to render")
        parser.add_argument(
            "outfname", help="pdf filename to create", nargs="?", default="")
        parser.add_argument(
            "path", help="path to work on", nargs="?", default=".")

    # add some options to the CLI:
    parser.add_argument("--debug", dest="debug", action="store_true",
                        help="increase logging level to DEBUG", default=False
                        )
    parser.add_argument("--version", dest="version",
                        help="show version and exit",
                        action="store_true", default=False)

    return parser


def main():
    '''
    The main. Initializes the stack, parses command line arguments, and fires
    requested logic.
    '''
    action = get_action(sys.argv)
    # print action
    parser = build_arg_parser(action)
    args = parser.parse_args()

    if args.version:
        print("payday {}".format(__version__))
        return 0

    if args.debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(level=level,
                        format='%(asctime)s %(levelname)s %(message)s')

    if action is None:
        parser.error(
            "Please specify a command: {}".format("|".join(VALID_ACTIONS)))

    if action == "list":
        from ..client import find_invoices
        for invoice in find_invoices(args.path):
            print("{}".format(invoice))
    elif action == "info":
        invoice = find_invoice(args.invoice_id, args.path)
        WARN_COLOR = "\033[93m"
        RESET_COLOR = "\033[0m"
        print(WARN_COLOR + invoice.path + RESET_COLOR)
        # print invoice.invoice
        import yaml
        yaml.safe_dump(
            invoice.invoice, sys.stdout, allow_unicode=True, encoding="utf-8")
    elif action == "render":
        if args.outfname == "":
            args.outfname = args.invoice_id + ".pdf"
        render_invoice(args.path, args.invoice_id, args.outfname)
    else:
        raise ValueError("invalid action '%s'" % action)

    return 0

if __name__ == '__main__':
    sys.exit(main())
