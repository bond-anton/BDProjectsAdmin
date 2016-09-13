from __future__ import division, print_function

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

from SPMonitor.Notebook import Notebook


class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # This will be in the windows group and have the "win" prefix
        max_action = Gio.SimpleAction.new_stateful("maximize", None,
                                                   GLib.Variant.new_boolean(False))
        max_action.connect("change-state", self.on_maximize_toggle)
        self.add_action(max_action)

        # Keep it in sync with the actual state
        self.connect("notify::is-maximized",
                     lambda obj, pspec: max_action.set_state(
                         GLib.Variant.new_boolean(obj.props.is_maximized)))

        #lbl_variant = GLib.Variant.new_string("String 1")
        #lbl_action = Gio.SimpleAction.new_stateful("change_label", lbl_variant.get_type(),
        #                                           lbl_variant)
        #lbl_action.connect("change-state", self.on_change_label_state)
        #self.add_action(lbl_action)
        #
        #self.label = Gtk.Label(label=lbl_variant.get_string(),
        #                       margin=30)
        #self.add(self.label)
        #self.label.show()

        self.notebook = Notebook()
        self.add(self.notebook)
        self.notebook.show()

    def on_change_label_state(self, action, value):
        action.set_state(value)
        self.label.set_text(value.get_string())

    def on_maximize_toggle(self, action, value):
        action.set_state(value)
        if value.get_boolean():
            self.maximize()
        else:
            self.unmaximize()
