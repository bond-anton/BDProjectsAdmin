from __future__ import division, print_function
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from SPMonitor import SPMApplication

from ScientificProjects.Client import Client

client = Client(config_file_name='config.ini')

app = SPMApplication()#client=client)
app.run(sys.argv)
