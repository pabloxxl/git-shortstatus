#!/usr/bin/env python

import argparse
import subprocess
import sys

VERSION = "0.1"
# Parse program arguments
parser = argparse.ArgumentParser(description="git-info v"+VERSION,
                                 epilog="developed by Pawel Cendrzak")

parser.add_argument('DIR', help='Git root directory',
                    nargs='?', default='~')

parser.add_argument("-d", "--debug",
                    help="enter debug mode",
                    action="store_true")

args = parser.parse_args()
pRoot = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

out, err = pRoot.communicate()
if err:
    print err.rstrip()
    sys.exit()

root = out.rstrip()

pStatus = subprocess.Popen(['git', 'status', root, '--porcelain'],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = pStatus.communicate()
if err:
    print err.rstrip()
    sys.exit()

status = out.rstrip()

if status:
    print status
else:
    print "Clean!"
