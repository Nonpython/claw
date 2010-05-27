#!/usr/bin/env python
"""This is my installer, I have it as a template, so I use it as a install
framework for my software."""
from shutil     import             copy
from shutil     import Error    as CopyError
from os         import             chmod, chown
from os         import getuid   as GetProcessUID
from stat       import             S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, \
                                           S_IWGRP, S_IXGRP
from sys        import exit     as die
from grp        import getgrnam as GetGroupStructByName
from pwd        import getpwnam as GetUserStructByName
import sqlite3, os, base64


# The Get?ID's Get?StructByName functions return a structure of
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

try:
    os.mkdir('/usr/share/btrfsguitools')
except:
    die('Something went wrong creating the directory "/usr/share/btrfsguitools"!')

conn = sqlite3.connect('/usr/share/btrfsguitools/snapshot.db')
c = conn.cursor()
c.execute("""CREATE TABLE snapshots (
	id INTEGER NOT NULL, 
	datestamp VARCHAR, 
	comment VARCHAR, 
	PRIMARY KEY (id)
);""")
conn.commit()
c.close()

open('/usr/share/btrfsguitools/icon.png','w').write(base64.decodestring("""iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACI0lEQVR4nH2TT0gUURzHP7PMyiPm
8A6LDdFhCINhDVnUQOifkAepToEksYHgHhWW8lQEgkIePEghdFAQspBQGEhhDyssuMFGHgw8TNBh
og4TeBjQ4IELvw4L0rqrDx48fvx+n9+/70NEOOtO3O6S2WxGzvOxRITTZ3L8lgwSozYjEgNuPkdg
FG+Wd6zTvm0BABt30qIN4GjwPe4ufm0JPhfw+WJalAE07AHjP4/bAlLtjFuPrgsacEC54LZNcQ7A
PYrxRgeJNRhHo3zN4viIbL+YbCm3LSCODaYS4iWQ7Ce4DkRBQGV9pdW53Wr2X09IvsOWfIctu1n7
5L3aaUv53mVZytrSssbtvrTkch4rpYggBs9uThTVYSHvoX5HmDqorgG6l3esFMBWd1qMgeJqxJzj
oQcaY5suDIALxcIopt/l7YEmRqMOQGdMg1zutWW3t1FqtdOW2Su2DD0ckqXn+SYFTj0tSDXryH6P
I/WPU1LtbbSRMkrDNR83P4aXgeF+zfCPGqXNUlMLY5U1YttAxhBMLUBhGgDrZqctcx6Q0bhK4bo+
5iBkT7mshDHvvvyy/r4aken1CsUuTW0vQvUPc//9JwsgtfPn2FpDE8YJCZDENULtE4QRc04MQLEa
UXQSagng+SfB8J+UX964KjnfQ8chup5ADH3fDq2NZ0/ELweUjgyJrZj5ftgs6dMamO9xZP6SLbMX
GkPafPxAyh/mz/zS/wBO0EvM0Q2OnAAAAABJRU5ErkJggg=="""))

# This sets the proper ownership and permissions.
try:
    chmod('/usr/sbin/btrfsguitools', S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | \
                                     S_IXGRP)
    chmod('/usr/share/btrfsguitools/snapshot.db', S_IRUSR | S_IWUSR | S_IRGRP \
                                                                                     | S_IWGRP)
    try:
        GID = GetGIDByName('wheel')
    except KeyError:
        GID = -1
    chown('/usr/sbin/btrfsguitools', GetUIDByName('root'), GID)
    chown('/usr/share/btrfsguitools/snapshot.db', GetUIDByName('root'), GID)
except OSError:
    die("There was a error setting the proper ownership and permission.")
