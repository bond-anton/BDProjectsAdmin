from __future__ import division, print_function

from os.path import dirname, realpath, join

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

from ScientificProjects.Client import Client
from SPMonitor.MainWindow import MainWindow
from SPMonitor.AboutWindow import AboutWindow, _version
from SPMonitor.PreferencesDialog import PreferencesDialog


class SPMApplication(Gtk.Application):
    def __init__(self, *args, **kwargs):
        #self.client = kwargs['client']
        super(SPMApplication, self).__init__(*args, application_id="org.projectx.spmonitor",
                                             flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                                             **kwargs)
        self.window = None

        self.add_main_option("test", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Command line test", None)
        self.add_main_option("version", ord("v"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Print version", None)

    def do_startup(self):
        dir_path = join(dirname(realpath(__file__)), 'xml')
        menu_ui_file = join(dir_path, 'app_menu.glade')

        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("preferences", None)
        action.connect("activate", self.on_preferences)
        self.add_action(action)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        builder = Gtk.Builder.new_from_file(menu_ui_file)
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = MainWindow(application=self, title="SPMonitor")
        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        if options.contains("test"):
            # This is printed on the main instance
            print("Test argument recieved")
        if options.contains("version"):
            # This is printed on the main instance
            print("SPMonitor v%s" % _version)
        else:
            self.activate()
        return 0

    def on_about(self, action, param):
        about_dialog = AboutWindow(transient_for=self.window, modal=True)
        about_dialog.show_all()
        about_dialog.present()

    def on_preferences(self, action, param):
        preferences_dialog = PreferencesDialog(self.window)
        preferences_dialog.show_all()
        preferences_dialog.present()
        preferences_dialog.read_in_config()
        response = preferences_dialog.run()

        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
            preferences_dialog.save_config()
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        preferences_dialog.destroy()

    def on_quit(self, action, param):
        self.quit()
