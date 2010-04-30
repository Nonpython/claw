#!/usr/bin/env python
import getopt, sys
class SQLAlchemyMagic:
    """Contains the universial magic for storing snapshots"""
    pass
class GTKGUIInterface(SQLAlchemyMagic):
    """Contains the GTK GUI code"""
    pass
class QtGUIInterface(SQLAlchemyMagic):
    """Contains the Qt GUI code"""
    pass
UI = {'GTK': GTKGUIInterface, 'Qt': QtGUIInterface}
UIClass = UI[getopt.getopt(sys.argv[1:], '', ['interface='])[0][0][1]]()
