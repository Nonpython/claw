#!/usr/bin/env python
import sqlalchemy, subprocess, time, sqlalchemy.orm, gtk
from sqlalchemy.ext.declarative import declarative_base as _Base
from sys                        import exit             as die

#Checks to see if the SQLAlchemy version is in the right range.
if  "0.6" not in sqlalchemy.__version__:
    die("Your SQLAlchemy is too old or too new!\nYou need 0.6.0 or newer \
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
        self.aysdialog = gtk.Dialog("Are you sure?",
            None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            (gtk.STOCK_NO, gtk.RESPONSE_REJECT,
            gtk.STOCK_YES, gtk.RESPONSE_ACCEPT))
        self.aysdialog.vbox.pack_start(gtk.Label("Are you sure you want to delete the snapshot?"))
        self.aysdialog.connect("response", self.response_callback)
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
      
    def responseToDialog(self, entry, dialog, response):
            dialog.response(response)
      
    def getText(self):
        dialog = gtk.MessageDialog(
        None,
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        gtk.MESSAGE_QUESTION,
        gtk.BUTTONS_OK,
        None)
        dialog.set_markup('Please enter your <b>comment</b>:')
        entry = gtk.Entry()
        entry.connect("activate", self.responseToDialog, dialog, gtk.RESPONSE_OK)
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label("Comment:"), False, 5, 5)
        hbox.pack_end(entry)
        dialog.format_secondary_markup("If it is empty, there is no comment")
        dialog.vbox.pack_end(hbox, True, True, 0)
        dialog.show_all()
        dialog.run()
        text = entry.get_text()
        dialog.destroy()
        return text

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
        tdstamp += ".%.2i:" % (timedate[3])
        tdstamp += "%i:" % (timedate[4])
        tdstamp += "%i" % (timedate[5])
        return tdstamp
    
    def to12(hour24):
        return (hour24 % 12) if (hour24 % 12) > 0 else 12

    def IsPM(hour24):
        return hour24 > 11

    def response_callback(self, dialog, response_id):
        self.aysdialog.hide_all()
        if responce_id == gtk.RESPONCE_ACCEPT:
            self.responce = True
        elif responce_id == gtk.RESPONCE_REJECT:
            self.responce = False
        else:
            self.responce = None
        return None

    def AddSnapshot(self):
        pbar.show()
        pbar.pulse()
        tdstamp = self.TimeStamper()
        comment = self.getText()
        subprocess.Popen("btrfsctl -s /claw-%s /" % (tdstamp), shell=True)
        DBSession.add(SQLAlchemyMagic(tdstamp, comment))
        DBSession.commit()
        pbar.set_fraction(0.0)
        pbar.hide()
        store.append(tdstamp, comment)
        
    def RMSnapshot(self):
        self.aysdialog.show_all()
        self.treeView.set_sensitive(False)
        while True:
            if not self.responce == None:
                break
        self.pbar.show()
        self.pbar.pulse()
        ToRM = DBSession.query(SQLAlchemyMagic).filter_by(
            timedate==datestamp).all()[0]
        DBSession.delete(ToRM)
        DBSession.commit()
        self.store.remove(self.treeView.get_selection().get_selected()[1])
        subprocess.Popen("btrfsctl -D /claw-%s /" % row[0], shell=True)
        

    def RunUI(self):
        self.connect("destroy", gtk.main_quit)
        self.set_title("Claw")
        self.set_icon_from_file("%s/share/btrfsguitools/claw.png" % (prefix))
        self.sw = gtk.ScrolledWindow()
        self.sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.store = gtk.ListStore(str, str)
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
                tdstamp += 'PM'
            else:
                tdstamp += 'AM'
            self.store.append(tdstamp, item.comment)
        self.treeView = gtk.TreeView(store)
        self.treeView.set_rules_hint(True)
        self.sw.add(self.treeView)
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Date", rendererText, text=0)
        column.set_sort_column_id(0)    
        self.treeView.append_column(column)
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Comment", rendererText, text=1)
        column.set_sort_column_id(1)
        self.treeView.append_column(column)
        rendererText = gtk.CellRendererText()
        self.bbox = gtk.HButtonBox()
        self.hbox = gtk.HBox(False, 50)
        self.pbar = gtk.ProgressBar()
        self.hbox.pack_start(pbar)
        self.bbox.set_layout(10)
        self.bbox.set_spacing(gtk.BUTTONBOX_END)
        self.button1 = gtk.Button('Create _New Snapshot')
        self.bbox.add(self.button1)
        self.button2 = gtk.Button('_Remove Existing Snapshot')
        self.bbox.add(self.button2)
        self.button1.connect("clicked", self.AddSnapshot)
        self.button2.connect("clicked", self.RMSnapshot)
        self.hbox.pack_start(bbox)
        self.vbox = gtk.VBox(False, 4)
        self.vbox.pack_start(self.hbox)
        self.vbox.pack_start(self.sw)
        self.add(self.vbox)
        self.show_all()
        self.pbar.hide()

UIClass  = UIInterface()
UIClass.RunUI()
gtk.main()