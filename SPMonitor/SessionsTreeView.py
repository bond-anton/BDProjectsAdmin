from __future__ import division, print_function

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ScientificProjects.Entities.Session import Session


class SessionsTreeView(Gtk.Box):

    def __init__(self):
        super(SessionsTreeView, self).__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        column_titles = ['User (token)', 'Opened', 'Host', 'Platform', 'Python', 'Project']

        self.sessions_treestore = Gtk.TreeStore(str, str, str, str, str, str, str, str, bool)

        self.treeview = Gtk.TreeView(self.sessions_treestore)

        for i, column_title in enumerate(column_titles):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i,
                                        foreground=6, background=7, foreground_set=8, background_set=8)
            self.treeview.append_column(column)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_vexpand(True)
        self.scrolled_window.add(self.treeview)
        self.scrolled_window_pos = 0

        self.treeview.connect('button_press_event', self.mouse_click)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.set_border_width(6)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        button = Gtk.Button()
        button.set_label('Close session')
        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        img = Gtk.Image.new_from_icon_name('window-close', Gtk.IconSize.BUTTON)
        button.set_image(img)
        button.set_always_show_image(True)
        button.connect('clicked', self.on_log_off_button_click)
        button_box.pack_start(button, False, True, 0)

        hbox.pack_start(button_box, False, True, 0)

        self.pack_start(self.scrolled_window, True, True, 0)
        self.pack_start(hbox, False, False, 0)

    def update_treeview(self, treeview):
        # first delete removed roots
        row_iter = self.sessions_treestore.get_iter_first()
        while row_iter is not None:
            user_name = self.sessions_treestore[row_iter][0]
            if user_name not in treeview:
                print('User %s has no opened session. Removing from list' % user_name)
                #  delete whole root
                self.sessions_treestore.remove(row_iter)
            else:
                if self.sessions_treestore.iter_has_child(row_iter):
                    child_iter = self.sessions_treestore.iter_children(row_iter)
                    while child_iter is not None:
                        session_name = self.sessions_treestore[child_iter][0]
                        session_found = False
                        for j in range(len(list(treeview[user_name]))):
                            if treeview[user_name][j][0] == session_name:
                                session_found = True
                                if self.sessions_treestore[child_iter][5] != treeview[user_name][j][5]:
                                    self.sessions_treestore[child_iter][5] = treeview[user_name][j][5]
                                break
                        if not session_found:
                            #  delete session
                            self.sessions_treestore.remove(child_iter)
                        child_iter = self.sessions_treestore.iter_next(child_iter)
                    for j in range(len(list(treeview[user_name]))):
                        session_name = treeview[user_name][j][0]
                        session_found = False
                        child_iter = self.sessions_treestore.iter_children(row_iter)
                        while child_iter is not None:
                            if self.sessions_treestore[child_iter][0] == session_name:
                                session_found = True
                                break
                            child_iter = self.sessions_treestore.iter_next(child_iter)
                        if not session_found:
                            #  append session
                            self.sessions_treestore.append(row_iter,
                                                           list(treeview[user_name][j]) + ['#000', '#fff', True])
            row_iter = self.sessions_treestore.iter_next(row_iter)

        for user_name in treeview.keys():
            user_found = False
            row_iter = self.sessions_treestore.get_iter_first()
            while row_iter is not None:
                if self.sessions_treestore[row_iter][0] == user_name:
                    user_found = True
                    break
                row_iter = self.sessions_treestore.iter_next(row_iter)
            if not user_found:
                parent_iter = self.sessions_treestore.append(None, [user_name] + [None] * 5 + ['#000', '#fff', True])
                for j in range(len(list(treeview[user_name]))):
                    self.sessions_treestore.append(parent_iter, list(treeview[user_name][j]) + ['#000', '#fff', True])

    def mouse_click(self, treeview, event):
        if event.button == 1:
            path, model, x, y = treeview.get_path_at_pos(int(event.x), int(event.y))
            # selection = treeview.get_selection()
            # (model, iter) = selection.get_selected()
            print(self.sessions_treestore[path][:])

    def on_log_off_button_click(self, widget):
        app_window = self.get_toplevel()
        client = app_window.application
        try:
            selection = self.treeview.get_selection()
            model, path = selection.get_selected()
            dialog = Gtk.MessageDialog(app_window, 0, Gtk.MessageType.QUESTION,
                                       Gtk.ButtonsType.YES_NO, 'Are you sure?')
            if self.sessions_treestore[path][1]:
                dialog.format_secondary_text(
                    'You are about to close session #%s' % self.sessions_treestore[path][0])
            else:
                dialog.format_secondary_text(
                    'You are about to close all active sessions of user @%s' % self.sessions_treestore[path][0])
            response = dialog.run()
            if response == Gtk.ResponseType.YES:
                print("QUESTION dialog closed by clicking YES button")
                if self.sessions_treestore[path][1]:
                    print('Closing session:', self.sessions_treestore[path][0])
                    client.logoff_sessions_queue.put(self.sessions_treestore[path][0])
                else:
                    print('Kick off user:', self.sessions_treestore[path][0])
                    client.logoff_users_queue.put(self.sessions_treestore[path][0])
            elif response == Gtk.ResponseType.NO:
                print("QUESTION dialog closed by clicking NO button")
            dialog.destroy()
        except TypeError:
            dialog = Gtk.MessageDialog(app_window, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, 'Select users or sessions')
            dialog.format_secondary_text(
                'Please select users or individual sessions in the sessions list first.')
            dialog.run()
            dialog.destroy()
