from __future__ import division, print_function

from os import pardir
from os.path import dirname, realpath, join

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

from BDProjectsSessionsMonitor.MainWindow import MainWindow
from BDProjectsSessionsMonitor.AboutWindow import AboutWindow
from BDProjectsSessionsMonitor.PreferencesDialog import PreferencesDialog
from BDProjectsSessionsMonitor.Monitor import ClientThread


class SPSMApplication(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super(SPSMApplication, self).__init__(*args, application_id="org.projectx.spuadmin",
                                              **kwargs)
        self.logoff_users_queue = Queue()
        self.logoff_sessions_queue = Queue()
        self.client = None
        self.window = None

        self.add_main_option("test", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Command line test", None)
        self.add_main_option("version", ord("v"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Print version", None)

        dir_path = join(dirname(realpath(__file__)), pardir)
        self.config_file_name = join(dir_path, 'config.ini')

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
            self.window = MainWindow(application=self, title="SPAdminTools")
            self.window.connect("delete-event", self.on_quit)
        self.window.present()
        self.restart_client_loop()

    def on_about(self, action, param):
        about_dialog = AboutWindow(transient_for=self.window, modal=True)
        about_dialog.present()

    def on_preferences(self, action, param):
        preferences_dialog = PreferencesDialog(self.window, config_file_name=self.config_file_name)
        preferences_dialog.present()
        response = preferences_dialog.run()
        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
            need_clent_restart = preferences_dialog.save_config()
            preferences_dialog.destroy()
            if need_clent_restart:
                self.restart_client_loop()
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
            preferences_dialog.destroy()
            if self.client is None:
                self.start_client_loop()

    def on_quit(self, action, param):
        print('Doing cleanup!')
        self.stop_client_loop()
        self.quit()

    def restart_client_loop(self):
        self.stop_client_loop()
        self.start_client_loop()

    def start_client_loop(self):
        if self.client is None:
            print('Starting client loop')
            try:
                self.client = ClientThread(config_file_name=self.config_file_name,
                                           sessions_treeview=self.window.sessions_treeview,
                                           logoff_users_queue=self.logoff_users_queue,
                                           logoff_sessions_queue=self.logoff_sessions_queue)
                self.client.start()
            except ValueError:
                print('Config file error reported by ClientThread')
                self.on_preferences(None, None)

    def stop_client_loop(self):
        if self.client is not None:
            print('Stopping client loop')
            self.client.join()
            self.client = None
