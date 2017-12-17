# -*- coding: utf-8 -*-

"""CLI program for clients."""


import sys
import logging

from .. import __version__

VALID_ACTIONS = set(("add", "list"))


def get_action(args):
    "Validate the user supplied action from the args list."
    for i, arg in enumerate(args):
        if arg in VALID_ACTIONS:
            del args[i]
            return arg
    return None


def build_arg_parser(action):
    import argparse
    import os
    usage = "%%(prog)s [%s] [--help] [options] ..." % "|".join(
        VALID_ACTIONS)
    epilog = "\nSee '%s <command> --help' for more information on a specific command.\n\n" % os.path.basename(
        sys.argv[0])
    parser = argparse.ArgumentParser(usage=usage, epilog=epilog)

    # example on how we could extend the parser:
    if action == "list":
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
        from payday.client import find_clients
        for client in find_clients(args.path):
            print("{}".format(client))
    elif action == "add":
        raise NotImplementedError("add is not yet implemented")

    return 0


if __name__ == '__main__':
    sys.exit(main())
