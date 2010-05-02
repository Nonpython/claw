#!/usr/bin/env python
import getopt, sys, os, sqlalchemy, sqlalchemy.orm, sys, gtk
from sqlalchemy.ext.declarative import declarative_base as _Base

#Checks to see if the SQLAlchemy version is in the right range.
if  "0.6" not in sqlalchemy.__version__:
    sys.exit("Your SQLAlchemy is too old or too new!\nYou need 0.6.0 or newer but older then 0.7.0.")

#Converts the magic function to the magic class.
_Base = _Base()

# This flag gets funged by the installer to denote the install status of the
# program.
installed = False


if not installed: # Checks if the source has been funged by the installer
    engine = sqlalchemy.create_engine('sqlite://')  # 'sqlite://' is a magic
                                                    # phrase to tell SQLAlchemy
                                                    # to keep the SQLite databse
                                                    # in memory.
else: # If this happens it has been funged by the installer, so I can talk to
      # the existing SQLite database.
    engine = sqlalchemy.create_engine('sqlite:////usr/share/btrfsguitools/snapshot.db')

class SQLAlchemyMagic(_Base, object):
    """Uses SQLAlchemy's declarative extension to map a database to a Python class in order to store btrfs snapshots."""
    # Sets up the table.
    __tablename__  = "snapshots"
    self.id        = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    self.datestamp = sqlalchemy.Column(sqlalchemy.String)
    self.comment   = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, date, comment):
        self.date = date
        self.comment = comment
        
    def __repr__(self):
        return "<SnapshotTableMap (Date: %s, Comment: %s)>" % (self.date, (self.comment or "None"))

class GTKGUIInterface(object):
    """Contains the GTK GUI code and connective glue for SQLAlchemy."""
    def __init__(self):
        self.DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
        self.KnownItems = []

UIClass  =  GTKGUIInterface()

UIClass.runUI()