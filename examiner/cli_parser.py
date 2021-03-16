"""
Parses all custom options and arguments
"""
import argparse

def parse():
    """
    Handles the arguments and options.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    group = parser.add_mutually_exclusive_group()

    # create the parser for the "tags" command
    group.add_argument(
        "-t", "--tags", dest="tags", default=[],
        nargs="+", help="collects tags to run specific tests"
    )

    args, _empty = parser.parse_known_args()
    return args
