#!/usr/bin/env python
import getopt
import sys
sys.path.append()
interface = getopt.getopt(sys.argv[1:], '', ['interface='])[0][0][1]
getattr(guisupport, interface)