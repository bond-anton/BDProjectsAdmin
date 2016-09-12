from __future__ import division, print_function

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from SPMonitor import MainWindow

from ScientificProjects.Client import Client

client = Client(config_file_name='config.ini')

win = MainWindow(client=client)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
