from __future__ import division, print_function

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class LogTreeView(Gtk.ScrolledWindow):

    def __init__(self):

        software_list = [("Firefox", 2002, "C++"),
                         ("Eclipse", 2004, "Java"),
                         ("Pitivi", 2004, "Python"),
                         ("Netbeans", 1996, "Java"),
                         ("Chrome", 2008, "C++"),
                         ("Filezilla", 2001, "C++"),
                         ("Bazaar", 2005, "Python"),
                         ("Git", 2005, "C"),
                         ("Linux Kernel", 1991, "C"),
                         ("GCC", 1987, "C"),
                         ("Frostwire", 2004, "Java")]

        self.software_liststore = Gtk.ListStore(str, int, str)
        for software_ref in software_list:
            self.software_liststore.append(list(software_ref))

        # creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView(self.software_liststore)
        for i, column_title in enumerate(["Software", "Release Year", "Programming Language"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        Gtk.ScrolledWindow.__init__(self)
        self.set_vexpand(True)
        self.add(self.treeview)

