from __future__ import division, print_function

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SessionsTreeView(Gtk.Box):

    def __init__(self):
        super(SessionsTreeView, self).__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        column_titles = ['User (token)', 'Opened', 'Host', 'Platform', 'Python']

        self.sessions_treestore = Gtk.TreeStore(str, str, str, str, str, str, str, bool)

        self.treeview = Gtk.TreeView(self.sessions_treestore)

        for i, column_title in enumerate(column_titles):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i,
                                        foreground=5, background=6, foreground_set=7, background_set=7)
            self.treeview.append_column(column)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_vexpand(True)
        self.scrolled_window.add(self.treeview)
        self.scrolled_window_pos = 0

        self.update_treeview([['Anton', ['xxxx', 'date', 'host', 'platform', 'python']]])

        self.pack_start(self.scrolled_window, True, True, 0)

    def update_treeview(self, treeview):
        # first delete removed roots
        row_iter = self.sessions_treestore.get_iter_first()
        while row_iter:
            print(self.sessions_treestore.get(row_iter))
            row_iter = self.sessions_treestore.iter_next(row_iter)

        for i in range(len(list(treeview))):

            parent_iter = self.sessions_treestore.append(None, [treeview[i][0]] + [None] * 4 + ['#000', '#fff', True])
            for j in range(1, len(list(treeview[i]))):
                self.sessions_treestore.append(parent_iter, list(treeview[i][j]) + ['#000', '#fff', True])

        for item in self.sessions_treestore:
            print(item)
