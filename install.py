#!/usr/bin/env python
from shutil import             copy
from os     import             chmod, chown
from os     import getuid   as GetProcessUID
from stat   import             S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IXGRP
from sys    import exit     as die
from grp    import getgrnam as GetGroupStructByName
from pwd    import getpwnam as GetUserStructByName

# The Get?ID's Get{Group|User}StructByName functions return a structure of
# useless (to us) information and one useful thing: the ?ID at the subscript [2].

def GetGID(name):
    return GetGroupStructByName(name)[2]

def GetUID(name):
    return GetUserStructByName(name)[2]

# This needs to be run by root, and this tests if it is running as root.
if GetProcessUID() != GetUID('root'):
    die("This must be run by root!\nQuitting...")
    
try:
    import sqlalchemy
    if '0.6' not in sqlalchemy.__version__:
        die("Your SQLAlchemy is too old or too new!\nYou need 0.6.0 or newer but older then 0.7.0.")
except ImportError:
    die("You need SQLAlchemy 0.6.0 or newer but a older version then 0.7.0.")

try:
    import gtk
except ImportError:
    die("You need PyGTK 2.10 or newer, preferably 2.12 or newer.")

# This copies the file to the right location.
copy('./btrfsguitools.py', '/usr/sbin/btrfsguitools')

# This funges the file so that it knows that it is installed.
btrfsguitools = open('/usr/sbin/btrfsguitools.py', 'r').readlines()
btrfsguitools[13] = 'installed = True\n'
open('/usr/sbin/btrfsguitools.py', 'w').writelines(btrfsguitools)

# This sets the proper ownership and permissions.
chmod('/usr/sbin/btrfsguitools', S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | \
                                 S_IXGRP)
chown('/usr/sbin/btrfsguitools', GetUID('root'), GetGID('wheel'))



# Some people may want a wrapper that automaticlly uses {gksu|kdesu} for them.
if raw_input('Do you want a wrapper?'):
