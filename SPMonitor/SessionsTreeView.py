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

        self.treeview.connect('button_press_event', self.mouse_click)

        self.pack_start(self.scrolled_window, True, True, 0)

    def update_treeview(self, treeview):
        # first delete removed roots
        row_iter = self.sessions_treestore.get_iter_first()
        user_name = None
        while row_iter is not None:
            user_name = self.sessions_treestore[row_iter][0]
            user_found = False
            #print('User:', self.sessions_treestore[row_iter][0])
            for i in range(len(list(treeview))):
                if treeview[i][0] == user_name:
                    user_found = True
                    break
            if not user_found:
                #  delete whole root
                self.sessions_treestore.remove(row_iter)
            else:
                if self.sessions_treestore.iter_has_child(row_iter):
                    child_iter = self.sessions_treestore.iter_children(row_iter)
                    while child_iter is not None:
                        session_name = self.sessions_treestore[child_iter][0]
                        session_found = False
                        #print('\tSession:', self.sessions_treestore[child_iter][0])
                        for j in range(1, len(list(treeview[i]))):
                            if treeview[i][j][0] == session_name:
                                session_found = True
                                break
                        if not session_found:
                            #  delete session
                            self.sessions_treestore.remove(child_iter)
                        child_iter = self.sessions_treestore.iter_next(child_iter)
                    for j in range(1, len(list(treeview[i]))):
                        session_name = treeview[i][j][0]
                        session_found = False
                        child_iter = self.sessions_treestore.iter_children(row_iter)
                        while child_iter is not None:
                            if self.sessions_treestore[child_iter][0] == session_name:
                                session_found = True
                                break
                            child_iter = self.sessions_treestore.iter_next(child_iter)
                        if not session_found:
                            #  append session
                            self.sessions_treestore.append(row_iter, list(treeview[i][j]) + ['#000', '#fff', True])
            row_iter = self.sessions_treestore.iter_next(row_iter)

        for i in range(len(list(treeview))):
            user_name = treeview[i][0]
            user_found = False
            row_iter = self.sessions_treestore.get_iter_first()
            while row_iter is not None:
                if self.sessions_treestore[row_iter][0] == user_name:
                    user_found = True
                    break
                row_iter = self.sessions_treestore.iter_next(row_iter)
            if not user_found:
                parent_iter = self.sessions_treestore.append(None, [user_name] + [None] * 4 + ['#000', '#fff', True])
                for j in range(1, len(list(treeview[i]))):
                    self.sessions_treestore.append(parent_iter, list(treeview[i][j]) + ['#000', '#fff', True])

    def mouse_click(self, treeview, event):
        if event.button == 3:
            path, model, x, y = treeview.get_path_at_pos(int(event.x), int(event.y))
            # selection = treeview.get_selection()
            # (model, iter) = selection.get_selected()
            print(self.sessions_treestore[path][0])