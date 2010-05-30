#!/usr/bin/env python
import sys, os, sqlalchemy, sys, subprocess, time, sqlalchemy.orm, gtk
from sqlalchemy.ext.declarative import declarative_base as _Base
from sys                        import exit             as die

#Checks to see if the SQLAlchemy version is in the right range.
if  "0.6" not in sqlalchemy.__version__:
    sys.exit("Your SQLAlchemy is too old or too new!\nYou need 0.6.0 or newer \
but older then 0.7.0.")

#Converts the magic function to the magic class.
DeclarativeBase = _Base()

# This flag gets funged by the installer to denote the install status of the
# program.
installed = False

if not installed:
    die("This needs to be installed before you can use it.")

engine = sqlalchemy.create_engine(
    'sqlite:///%s/share/btrfsguitools/snapshot.db' % (prefix))

DBSession = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(
                                                         bind=engine))

class SQLAlchemyMagic(DeclarativeBase, object):
    "Uses SQLAlchemy's declarative extension to map a database to a Python" + \
    " class in order to store btrfs snapshots."
    # Sets up the table.
    __tablename__  = "snapshots"
    id              = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    timedate = sqlalchemy.Column(sqlalchemy.String)
    comment   = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, timedate, comment):
        self.timedate = timedate
        self.comment  = comment
        
    def __repr__(self):
        return "<SnapshotTableMap (Date: %s, Comment: %s)>" % (self.date,
                                                (self.comment or "None"))

class UIInterface(object, gtk.Window):
    "Contains the GTK GUI code and connective glue for SQLAlchemy."
    def __init__(self):
        super(UIInterface, self).__init__()
        self.metadata = DeclarativeBase.metadata
        # Checks the database for existing snapshots.
        self.KnownItems = [column for column in \
                           DBSession.query(SQLAlchemyMagic).all()]
        daysofweek = {'Mon': 'Monday, ', 'Tue': 'Tuesday, ',
                      'Wed': 'Wednesday, ', 'Thu': 'Thursday, ',
                      'Fri': 'Friday, ', 'Sat': 'Saturday, ',
                      'Sun': 'Sunday, '}
        monthsofyear ={'Jan': 'January ', 'Feb': 'Febuary ',
                       'Mar': 'March ', 'Apr': 'April ', 'May': 'May ',
                       'Jun': 'June ', 'Jul': 'July', 'Aug': 'August ',
                       'Sep': 'September ', 'Oct': 'October ',
                       'Nov': 'November', 'Dec': 'December '}
        numbersuffixes = {}
        for x in range(0,4):
            for y in range(0,10):
                if x == 0:
                    if y == 1:
                       numbersuffixes[int('%i' % (y))] = '%ist ' % (y)
                    elif y == 2:
                       numbersuffixes[int('%i' % (y))] = '%ind ' % (y)
                    elif y == 3:
                       numbersuffixes[int('%i' % (y))] = '%ird ' % (y)
                    elif y >= 4:
                       numbersuffixes[int('%i' % (y))] = '%ith ' % (y)
                elif x == 1:
                    numbersuffixes[int('%i%i' % (x, y))] = '%i%ith ' % \
                                                                  (x, y)
                elif x == 2:
                    if y == 0:
                        numbersuffixes[int('%i%i' % (x, y))] = '%i%ith ' % \
                                                                      (x, y)
                    elif y == 1:
                       numbersuffixes[int('%i%i' % (x, y))] = '%i%ist ' % \
                                                                     (x, y)
                    elif y == 2:
                       numbersuffixes[int('%i%i' % (x, y))] = '%i%ind ' % \
                                                                     (x, y)
                    elif y == 3:
                       numbersuffixes[int('%i%i' % (x, y))] = '%i%ird ' % \
                                                                     (x, y)
                    elif y >= 4:
                       numbersuffixes[int('%i%i' % (x, y))] = '%i%ith ' % \
                                                                     (x, y)
                elif x == 3:
                    if y == 0:
                        numbersuffixes[int('%i%i' % (x, y))] = '%i%ith ' % \
                                                                      (x, y)
                    elif y == 1:
                       numbersuffixes[int('%i%i' % (x, y))] = '%i%ist ' % \
                                                                     (x, y)

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
        tdstamp += ",%2i:" % (timedate[3])
        tdstamp += "%i:" % (timedate[4])
        tdstamp += "%i" % (timedate[5])
        return tdstamp
    
    def to12(hour24):
        return (hour24 % 12) if (hour24 % 12) > 0 else 12

    def IsPM(hour24):
        return hour24 > 11


    def AddSnapshot(self, comment):
        pbar.show()
        pbar.pulse()
        tdstamp = self.TimeStamper()
        subprocess.Popen("btrfsctl -s /claw-%s /" % (tdstamp), shell=True)
        DBSession.add(SQLAlchemyMagic(tdstamp, comment))
        DBSession.commit()
        pbar.set_fraction(0.0)
        pbar.hide()
        store.append(tdstamp, comment)
        
    def RMSnapshot(self, datestamp):
        pbar.show()
        pbar.pulse()
        ToRM = DBSession.query(SQLAlchemyMagic).filter_by(
            timedate==datestamp).all()[0]
        DBSession.delete(ToRM)
        DBSession.commit()
        for row in store:
            if row[0] == datestamp:
                subprocess.Popen("btrfsctl -D /claw-%s /" % row[0], shell=True)
        

    def RunUI(self):
        self.connect("destroy", gtk.main_quit)
        self.set_title("Claw")
        self.set_icon_from_file("%s/share/btrfsguitools/claw.png" % (prefix))
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        store = gtk.ListStore(str, str)
        for item in self.KnownItems:
            timein = item.timedate
            tdstamp = ''
            tdstamp += daysofweek[timein[0:3]]
            tdstamp += monthsofyear[timein[3:6]]
            # Get date from datestamp 
            tdstamp += '%s ' % (timein[6:8])
            # Get time from the datestamp
            tdstamp += '%i:%s ' % (self.to12(int(timein[9:11])), timein[12:14])
            if self.IsPM(timein[9:11]):
                tdstamp += 'PM '
            else:
                tdstamp += 'AM '
            store.append(tdstamp, item.comment)
        treeView = gtk.TreeView(store)
        treeView.connect("row-activated", self.on_activated)
        treeView.set_rules_hint(True)
        sw.add(treeView)
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Date", rendererText, text=0)
        column.set_sort_column_id(0)    
        treeView.append_column(column)
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Place", rendererText, text=1)
        column.set_sort_column_id(1)
        treeView.append_column(column)
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Year", rendererText, text=2)
        column.set_sort_column_id(2)
        treeView.append_column(column)
        bbox = gtk.HButtonBox()
        hbox = gtk.HBox(False, 50)
        pbar = gtk.ProgressBar()
        hbox.pack_start(pbar)
        bbox.set_layout(10)
        bbox.set_spacing(gtk.BUTTONBOX_END)
        bbox.add(gtk.Button('Create _New Snapshot'))
        bbox.add(gtk.Button('_Remove Existing Snapshot'))
        hbox.pack_start(bbox)
        vbox = gtk.VBox(False, 4)
        vbox.pack_start(hbox)
        vbox.pack_start(sw)
        self.add(vbox)
        self.show_all()
        pbar.hide()
        gtk.main()

UIClass  = UIInterface()

UIClass.RunUI()
