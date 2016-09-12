from __future__ import division, print_function

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from SPMonitor.Notebook import Notebook


class MainWindow(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title='SPMonitor')
        self.set_border_width(3)

        self.notebook = Notebook()
        self.add(self.notebook)
