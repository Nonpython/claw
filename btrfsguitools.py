#!/usr/bin/env python
import getopt, sys
import sqlalchemy
if  "0.6" not in sqlalchemy.__version__:
    sys.exit("Your SQLAlchemy is too old!\nYou need 0.6.0 or newer but older then 0.7.0.")
class SQLAlchemyMagic:
    """Contains the universial magic for storing snapshots"""
    def __init__(self):
        self.SqliteDB = create_engine('sqlite:////usr/share/btrfsguitools/snapshot.db')
        self.Metadata = sqlalchemy.MetaData()
        self.SnapshotTable = sqlalchemy.Table('snapshots', self.Metadata, \
                                                sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True), \
                                                sqlalchemy.Column('date', sqlalchemy.String(30)), \
                                                sqlalchemy.Column('comment', sqlalchemy.String), \
                                             )

    
class GTKGUIInterface(SQLAlchemyMagic):
    """Contains the GTK GUI code"""
    pass
class QtGUIInterface(SQLAlchemyMagic):
    """Contains the Qt GUI code"""
    pass
UI = {'GTK': GTKGUIInterface, 'Qt': QtGUIInterface}
UIClass = UI[getopt.getopt(sys.argv[1:], '', ['interface='])[0][0][1]]()
