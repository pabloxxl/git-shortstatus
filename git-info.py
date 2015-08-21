#!/usr/bin/env python

import argparse

VERSION = "0.1"
# Parse program arguments
parser = argparse.ArgumentParser(description="git-info v"+VERSION,
                                 epilog="developed by Pawel Cendrzak")

parser.add_argument('COMMIT', help='commit to describe',
                    nargs='?', default='HEAD')

parser.add_argument("-d", "--debug",
                    help="enter debug mode",
                    action="store_true")

args = parser.parse_args()
print args.COMMIT
