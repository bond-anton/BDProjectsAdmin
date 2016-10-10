from __future__ import division, print_function

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

from SPSessionsMonitor.SessionsTreeView import SessionsTreeView


class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        for key in ['application']:
            if key in kwargs:
                setattr(self, key, kwargs[key])
        super(MainWindow, self).__init__(*args, **kwargs)
        self.set_default_size(1050, 480)
        # This will be in the windows group and have the "win" prefix
        max_action = Gio.SimpleAction.new_stateful("maximize", None,
                                                   GLib.Variant.new_boolean(False))
        max_action.connect("change-state", self.on_maximize_toggle)
        self.add_action(max_action)

        # Keep it in sync with the actual state
        self.connect("notify::is-maximized",
                     lambda obj, pspec: max_action.set_state(
                         GLib.Variant.new_boolean(obj.props.is_maximized)))

        self.sessions_treeview = SessionsTreeView()
        self.add(self.sessions_treeview)
        self.set_default_icon_name('system-users')
        self.show_all()

    def on_change_label_state(self, action, value):
        action.set_state(value)
        self.label.set_text(value.get_string())

    def on_maximize_toggle(self, action, value):
        action.set_state(value)
        if value.get_boolean():
            self.maximize()
        else:
            self.unmaximize()
