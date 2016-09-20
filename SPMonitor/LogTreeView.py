from __future__ import division, print_function

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class LogTreeView(Gtk.Box):

    def __init__(self):
        super(LogTreeView, self).__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        column_titles = ['Date', 'Type', 'User', 'Project', 'Message']

        self.log_liststore = Gtk.ListStore(str, str, str, str, str)

        # creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView(self.log_liststore)
        for i, column_title in enumerate(column_titles):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.add(self.treeview)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.set_border_width(6)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        Gtk.StyleContext.add_class(button_box.get_style_context(), "linked")
        self.buttons = dict()
        for log_type in ['Error', 'Warning', 'Information']:
            grid = Gtk.Grid()
            button = Gtk.ToggleButton()
            img = Gtk.Image.new_from_icon_name('dialog-' + log_type.lower(), Gtk.IconSize.BUTTON)
            label = Gtk.Label(log_type)
            grid.attach(img, 0, 0, 1, 1)
            grid.attach(label, 0, 1, 1, 1)
            grid.show_all()
            button.add(grid)
            button.set_active(True)
            self.buttons[log_type] = button
            button.connect('clicked', self.on_selection_button_clicked)
            button_box.pack_start(button, False, True, 0)
        button = Gtk.Button()
        grid = Gtk.Grid()
        img = Gtk.Image.new_from_icon_name('view-refresh', Gtk.IconSize.BUTTON)
        label = Gtk.Label('All')
        grid.attach(img, 0, 0, 1, 1)
        grid.attach(label, 0, 1, 1, 1)
        grid.show_all()
        button.add(grid)
        button.set_label('All')
        self.buttons['All'] = button
        button.connect('clicked', self.on_selection_button_clicked)
        button_box.pack_start(button, False, True, 0)

        pager_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label = Gtk.Label("1")
        pager_box.pack_start(label, False, True, 0)
        label = Gtk.Label("-")
        pager_box.pack_start(label, False, True, 0)
        label = Gtk.Label("10")
        pager_box.pack_start(label, False, True, 0)
        label = Gtk.Label("of")
        pager_box.pack_start(label, False, True, 0)
        label = Gtk.Label('1000')
        pager_box.pack_start(label, False, True, 0)
        pager_box.set_halign(Gtk.Align.END)

        pager_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        Gtk.StyleContext.add_class(pager_button_box.get_style_context(), "linked")
        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        button.connect('clicked', self.on_left_pager_button_clicked)
        pager_button_box.pack_start(button, False, True, 0)

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        button.connect('clicked', self.on_right_pager_button_clicked)
        pager_button_box.pack_start(button, False, True, 0)
        pager_box.pack_start(pager_button_box, False, True, 0)

        hbox.pack_start(button_box, False, True, 0)
        hbox.pack_start(pager_box, True, True, 0)

        self.pack_start(hbox, False, False, 0)
        self.pack_start(scrolled_window, True, True, 0)

    def add_record(self, record):
        self.log_liststore.append(list(record))

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        for label in self.buttons.keys():
            if self.buttons[label] == widget:
                if label == 'All':
                    print('All log types selected')
                    for button in self.buttons.values():
                        try:
                            button.set_active(True)
                        except AttributeError:
                            pass
                else:
                    if widget.get_active():
                        print('%s log type selected!' % label)
                    else:
                        print('%s log type unselected!' % label)

    def on_left_pager_button_clicked(self, widget):
        print('<<')

    def on_right_pager_button_clicked(self, widget):
        print('>>')
