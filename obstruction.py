#!/bin/env python3

import argparse
import sys
from ipaddress import ip_address
from connection import Config


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--create", action="store_true", default=False,
                       help="returns ip address, which will be necessary for "
                            "establishing connection with other player "
                            "(port 5000 and above pretends to be safe) "
                            "requires '--port' argument")
    group.add_argument("--connect", nargs=1, type=ip_address,
                       help="requires ip address to connect to the game and "
                            "'--port' argument",
                       metavar="IP ADDRESS")
    parser.add_argument("--port", nargs=1, type=int, help="port number",
                        metavar="PORT")
    args = parser.parse_args()

    if (args.create or args.connect is not None) and args.port is None:
        parser.error("'--create' and '--connect' requires '--port'")

    init = Config()
    try:
        init.init_game(args.create, args.connect, args.port)
    except OSError as err:
        sys.exit(err)


if __name__ == '__main__':
    main()
