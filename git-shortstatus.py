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
    class statusItem(object):
        def __init__(self, txt, type):
            self.txt = txt
            self.type = type

    def __init__(self):
        self.statusList = []

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

        status = out.rstrip().split("\n")
        for item in status:
            type, name = item.split()
            self.statusList.append(self.statusItem(name, type))

        # TODO Add sorting to directories
        return code.OK

    def getModified(self):
        return [a.txt for a in self.statusList if a.type == "M"]

    def getDeleted(self):
        return [a.txt for a in self.statusList if a.type == "D"]

    def getNew(self):
        return [a.txt for a in self.statusList if a.type == "N"]

    def getAll(self):
        return [a.txt for a in self.statusList]

if __name__ == "__main__":
    s = shortStatus()
    returnCode = s.parse()
    if returnCode:
        print "Git shortstatus returned code " + str(returnCode)
        sys.exit(returnCode)
    lMod = s.getModified()
    lDel = s.getDeleted()
    lNew = s.getNew()

    lModLen = len(lMod)
    lDelLen = len(lDel)
    lNewLen = len(lNew)

    llen = lModLen + lDelLen + lNewLen
    print "Modified: " + str(lModLen)
    print "Deleted:  " + str(lDelLen)
    print "New:      " + str(lNewLen)
    print "------------"
    print "All:      " + str(llen)
    sys.exit(0)
