#!/usr/bin/env python
from shutil import copy
from os import chmod
from stat import S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IXGRP, S_IROTH, S_IXOTH
copy('./btrfsguitools.py', '/usr/sbin/btrfsguitools')
chmod('/usr/sbin/btrfsguitools', S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | \
                                 S_IXGRP | S_IROTH | S_IXOTH)
