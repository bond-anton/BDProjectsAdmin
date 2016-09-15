from __future__ import division, print_function

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from SPMonitor.LogTreeView import LogTreeView

class Notebook(Gtk.Notebook):

    def __init__(self):
        Gtk.Notebook.__init__(self)

        self.page1 = Gtk.Grid()
        self.page1.set_column_homogeneous(True)
        self.page1.set_row_homogeneous(True)
        self.logs_treeview = LogTreeView()
        self.page1.attach(self.logs_treeview, 0, 0, 8, 10)
        self.append_page(self.page1, Gtk.Label('Log'))

        self.page2 = Gtk.Grid()
        self.page2.set_column_homogeneous(True)
        self.page2.set_row_homogeneous(True)
        self.sessions_treeview = LogTreeView()
        self.page2.attach(self.sessions_treeview, 0, 0, 8, 10)
        self.append_page(self.page2, Gtk.Label('Sessions'))
