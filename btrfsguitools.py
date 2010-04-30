#!/usr/bin/env python
import getopt
import sys
import os
import sqlalchemy, sqlalchemy.orm, sys
from sqlalchemy.ext.declarative import declarative_base as _Base

if  "0.6" not in sqlalchemy.__version__:
    sys.exit("Your SQLAlchemy is too old or too new!\nYou need 0.6.0 or newer but older then 0.7.0.")

_Base = _Base()

installed = 0

if installed == 0:
    engine = sqlalchemy.create_engine('sqlite://')
else:
    engine = sqlalchemy.create_engine('sqlite:////usr/share/btrfsguitools/snapshot.db')

class SQLAlchemyMagic(object):
    __tablename__  = "snapshots"
    self.id        = sqlalchemy.Column(Integer, primary_key=True)
    self.datestamp = sqlalchemy.Column(String)
    self.comment   = sqlalchemy.Column(String)

    def __init__(self, date, comment):
        self.date = date
        self.comment = comment
        
    def __repr__(self):
        return "<SnapshotTableMap (Date: %s, Comment: %s)>" % (self.date, (comment or "None"))

class GTKGUIInterface(object):
    """Contains the GTK GUI code"""
    pass

class QtGUIInterface(object):
    """Contains the Qt GUI code"""
    pass

interface = getopt.getopt(sys.argv[1:], '', ['interface='])[0][0][1]
if interface == 'GTK':
    UIClass = GTKGUIInterface()
elif interface == 'Qt':
    UIClass = QtGUIInterface()
   
UIClass.runUI()