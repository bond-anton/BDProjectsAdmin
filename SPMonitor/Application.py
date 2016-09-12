from __future__ import division, print_function

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

from ScientificProjects.Client import Client
from SPMonitor.MainWindow import MainWindow


class SPMApplication(Gtk.Application):

    def __init__(self, client):
        assert isinstance(client, Client), 'Valid SP Client expected'
        self.client = client
        Gtk.Application.__init__(self, application_id='apps.projectx.pmmonitor',
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect('activate', self.on_activate)

    def on_activate(self, data=None):
        window = MainWindow()
        window.show_all()
        self.add_window(window)
