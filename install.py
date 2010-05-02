#!/usr/bin/env python
from shutil     import             copy
from shutil     import Error    as CopyError
from os         import             chmod, chown
from os         import getuid   as GetProcessUID
from stat       import             S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IXGRP
from sys        import exit     as die
from grp        import getgrnam as GetGroupStructByName
from pwd        import getpwnam as GetUserStructByName

# The Get?ID's Get{Group|User}StructByName functions return a structure of
# useless (to us) information and one useful thing: the ?ID at the subscript
# [2].

def GetGIDByName(name):
    return GetGroupStructByName(name)[2]

def GetUIDByName(name):
    return GetUserStructByName(name)[2]

# This needs to be run by root, and this tests if it is running as root.
if GetProcessUID() != GetUIDByName('root'):
    die("This must be run by root!\nQuitting...")
    
# Verifies that we have the correct versions of the correct libraries.
try:
    import sqlalchemy
    if '0.6' not in sqlalchemy.__version__:
        die("Your SQLAlchemy is too old or too new!\nYou need 0.6.0 or newer \
             but older then 0.7.0.")
except ImportError:
    die("You need SQLAlchemy 0.6.0 or newer but a older version then 0.7.0.")

try:
    import pygtk
    try:
        pygtk.require('2.10')
    except AssertionError:
        die()
except:
    die("You need PyGTK 2.10 or newer, preferably 2.12 or newer.")

# This copies the file to the right location.
try:
    copy('./btrfsguitools.py', '/usr/sbin/btrfsguitools')
except CopyError:
    die("There was a error installing the program.")

# This funges the file so that it knows that it is installed.
try:
    btrfsguitools = open('/usr/sbin/btrfsguitools.py', 'r').readlines()
    btrfsguitools[13] = 'installed = True\n'
    open('/usr/sbin/btrfsguitools.py', 'w').writelines(btrfsguitools)
except IOError:
    die("There was a error modifing the program after the installation.")

# This sets the proper ownership and permissions.
try:
    chmod('/usr/sbin/btrfsguitools', S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | \
                                     S_IXGRP)
    try:
        gid = GetGIDByName('wheel')
    except KeyError:
        gid = -1
    chown('/usr/sbin/btrfsguitools', GetUIDByName('root'), gid)
except OSError:
    die("There was a error setting the proper ownership and permission.")

# Some people may want a wrapper that automaticlly uses gksu[do]? for them.
if raw_input('Do you want a wrapper? [yn] ').lower() == 'y':
        open('/usr/bin/btrfsguitools', 'w').writelines(['#!/bin/sh\n',
                                                        'gksu \
                                                        /usr/sbin/btrfsguitools'
                                                        ])
