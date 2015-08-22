#!/usr/bin/env python

import argparse
import subprocess
import sys

VERSION = "0.1"


class code:
    OK = 0
    REV_PARSE_ERROR = 1
    GIT_STATUS_ERROR = 2
    UNSUPORTED_PARAM = 3


class shortStatus(object):

    def parse(self):
        # Parse program arguments
        parser = argparse.ArgumentParser(description="git-info v"+VERSION,
                                         epilog="developed by Pawel Cendrzak")

        parser.add_argument("--sum", "-s", "--debug",
                            help="enter debug mode",
                            action="store_true")

        args = parser.parse_args()
        if args.sum:
            return code.UNSUPORTED_PARAM
        pRoot = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        out, err = pRoot.communicate()
        if err:
            return code.REV_PARSE_ERROR

        root = out.rstrip()

        pStatus = subprocess.Popen(['git', 'status', root, '--porcelain'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        out, err = pStatus.communicate()
        if err:
            return code.GIT_STATUS_ERROR

        self.statusList = out.rstrip().split("\n")
        return code.OK

if __name__ == "__main__":
    s = shortStatus()
    returnCode = s.parse()
    if returnCode:
        print "Git shortstatus returned code " + str(returnCode)
        sys.exit(returnCode)
    sys.exit(0)
