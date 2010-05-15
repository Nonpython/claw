#!/usr/bin/env python
import getopt, sys, os, sqlalchemy, sys, gtk, subprocess, time, sqlalchemy.orm
from sqlalchemy.ext.declarative import declarative_base as _Base

#Checks to see if the SQLAlchemy version is in the right range.
if  "0.6" not in sqlalchemy.__version__:
    sys.exit("Your SQLAlchemy is too old or too new!\nYou need 0.6.0 or newer \
but older then 0.7.0.")

#Converts the magic function to the magic class.
DeclarativeBase = _Base()

# This flag gets funged by the installer to denote the install status of the
# program.
installed = False


if not installed: # Checks if the source has been funged by the installer
    engine = sqlalchemy.create_engine('sqlite://')  # 'sqlite://' is a magic
                                                    # phrase to tell SQLAlchemy
                                                    # to keep the SQLite
                                                    # database in memory.
else: # If this happens it has been funged by the installer, so I can talk to
      # the existing SQLite database.
    engine = sqlalchemy.create_engine(
        'sqlite:////usr/share/btrfsguitools/snapshot.db')

DBSession = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(
                                                         bind=engine))

class SQLAlchemyMagic(DeclarativeBase, object):
    "Uses SQLAlchemy's declarative extension to map a database to a Python" + \
    " class in order to store btrfs snapshots."
    # Sets up the table.
    __tablename__  = "snapshots"
    id              = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    datestamp = sqlalchemy.Column(sqlalchemy.String)
    comment   = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, date, comment):
        self.date          = date
        self.comment  = comment
        
    def __repr__(self):
        return "<SnapshotTableMap (Date: %s, Comment: %s)>" % (self.date,
                                                (self.comment or "None"))

class GTKGUIInterface(object):
    "Contains the GTK GUI code and connective glue for SQLAlchemy."
    def __init__(self):
        self.metadata = DeclarativeBase.metadata
        if not installed:
            self.metadata.create_all(engine)
        # Checks the database for existing snapshots.
        self.KnownItems = []
        for column in DBSession.query(SQLAlchemyMagic).all():
            self.KnownItems.append(column)

    def TimeStamper(self):
        timedate = time.localtime()
        tdstamp = ''
        # This is a nifty little hack that greatly speeds
        # up the generation of the datestamp.
        tdstamp += ["Mon",  "Tue", "Wed", "Thu",  \
                            "Fri", "Sat", "Sun"][timedate[6]]
        # The -1 is needed because
        # the time.struct_time's month
        # field counts from 1, while
        # python sequence subscripts
         # count from 0.
        tdstamp += ["Jan", "Feb", "Mar", "Apr", "May", \
                            "Jun", "Jul", "Aug", "Sep", "Oct", \
                            "Nov", "Dec"][timedate[1]-1]
        tdstamp += str(timedate[2])
        tdstamp += ",%i:" % (timedate[3])
        tdstamp += "%i:" % (timedate[4])
        tdstamp += "%i" % (timedate[5])
        return tdstamp

    def AddDBItem(self, comment):
        subprocess.Popen("btrfsctl " + \
                         "-s btrfsguitools-%s /" % (tdstamp), shell=True)
        DBSession.add( SQLAlchemyMagic(self.TimeStamper(), comment))
        DBSession.commit()
        
    def RunUI(self):
        pass

UIClass  = GTKGUIInterface()

UIClass.RunUI()
