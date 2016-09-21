from __future__ import division, print_function

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class LogTreeView(Gtk.Box):

    def __init__(self):
        super(LogTreeView, self).__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        column_titles = ['Date', 'Type', 'User', 'Project', 'Message']

        self.log_liststore = Gtk.ListStore(str, str, str, str, str, str, str, bool)

        # Creating the filter, feeding it with the liststore model
        self.log_category_filter = self.log_liststore.filter_new()
        # setting the filter function, note that we're not using the
        self.log_category_filter.set_visible_func(self.log_category_filter_func)
        self.current_filter_category = ['Error', 'Warning', 'Information']

        # creating the treeview, making it use the filter as a model, and adding the columns
        #self.treeview = Gtk.TreeView(self.log_liststore)
        self.treeview = Gtk.TreeView.new_with_model(self.log_category_filter)

        self.treeview.connect('size-allocate', self.treeview_changed)

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

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.set_border_width(6)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        Gtk.StyleContext.add_class(button_box.get_style_context(), "linked")
        self.buttons = dict()
        for log_type in ['Error', 'Warning', 'Information']:
            grid = Gtk.Grid()
            grid.set_column_spacing(5)
            button = Gtk.ToggleButton()
            img = Gtk.Image.new_from_icon_name('dialog-' + log_type.lower(), Gtk.IconSize.BUTTON)
            label = Gtk.Label(log_type)
            grid.attach(img, 0, 0, 1, 1)
            grid.attach(label, 1, 0, 1, 1)
            grid.show_all()
            button.add(grid)
            button.set_active(True)
            self.buttons[log_type] = button
            button.connect('clicked', self.on_selection_button_clicked)
            button_box.pack_start(button, False, True, 0)
        button = Gtk.Button()
        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        img = Gtk.Image.new_from_icon_name('view-refresh', Gtk.IconSize.BUTTON)
        label = Gtk.Label('All')
        grid.attach(img, 0, 0, 1, 1)
        grid.attach(label, 1, 0, 1, 1)
        grid.show_all()
        button.add(grid)
        self.buttons['All'] = button
        button.connect('clicked', self.on_selection_button_clicked)
        button_box.pack_start(button, False, True, 0)

        pager_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.pager_label = Gtk.Label('no data... ')
        pager_box.pack_start(self.pager_label, False, True, 0)
        pager_box.set_halign(Gtk.Align.END)

        pager_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        Gtk.StyleContext.add_class(pager_button_box.get_style_context(), "linked")
        button = Gtk.Button()
        img = Gtk.Image.new_from_icon_name('go-top', Gtk.IconSize.BUTTON)
        button.add(img)
        button.connect('clicked', self.on_go_top_pager_button_clicked)
        pager_button_box.pack_start(button, False, True, 0)

        button = Gtk.Button()
        img = Gtk.Image.new_from_icon_name('go-up', Gtk.IconSize.BUTTON)
        button.add(img)
        button.connect('clicked', self.on_go_up_pager_button_clicked)
        pager_button_box.pack_start(button, False, True, 0)

        button = Gtk.Button()
        img = Gtk.Image.new_from_icon_name('go-down', Gtk.IconSize.BUTTON)
        button.add(img)
        button.connect('clicked', self.on_go_down_pager_button_clicked)
        pager_button_box.pack_start(button, False, True, 0)

        button = Gtk.Button()
        img = Gtk.Image.new_from_icon_name('go-bottom', Gtk.IconSize.BUTTON)
        button.add(img)
        button.connect('clicked', self.on_go_bottom_pager_button_clicked)
        pager_button_box.pack_start(button, False, True, 0)
        pager_box.pack_start(pager_button_box, False, True, 0)

        hbox.pack_start(button_box, False, True, 0)
        hbox.pack_start(pager_box, True, True, 0)

        self.pack_start(self.scrolled_window, True, True, 0)
        self.pack_start(hbox, False, False, 0)

    def add_record(self, record):
        self.log_liststore.insert(0, list(record))

    def on_go_top_pager_button_clicked(self, widget):
        print('|<')
        adj = self.scrolled_window.get_vadjustment()
        adj.set_value(0)
        self.recalculate_table_position()

    def on_go_up_pager_button_clicked(self, widget):
        print('<<')
        adj = self.scrolled_window.get_vadjustment()
        adj.set_value(adj.get_value() - adj.get_page_size())
        self.recalculate_table_position()

    def on_go_down_pager_button_clicked(self, widget):
        print('>>')
        adj = self.scrolled_window.get_vadjustment()
        adj.set_value(adj.get_value() + adj.get_page_size())
        self.recalculate_table_position()

    def on_go_bottom_pager_button_clicked(self, widget):
        print('>|')
        adj = self.scrolled_window.get_vadjustment()
        if adj.get_value() < adj.get_minimum_increment():
            adj.set_value(adj.get_upper() - adj.get_page_size())
        self.recalculate_table_position()

    def treeview_changed(self, widget, event, data=None):
        adj = self.scrolled_window.get_vadjustment()
        if adj.get_value() < adj.get_minimum_increment():
            adj.set_value(0)
        self.recalculate_table_position()

    def recalculate_table_position(self):
        adj = self.scrolled_window.get_vadjustment()
        print('Recalculating log table position')
        path = Gtk.TreePath().new_first()
        row_height = self.treeview.get_cell_area(path).height
        list_length = len(self.log_liststore)
        try:
            num_rows = adj.get_page_size() / row_height - 1
            if list_length > num_rows:
                first_row = int(adj.get_value() / row_height) + 1
                last_row = first_row + num_rows
            else:
                first_row = 1
                last_row = list_length
                num_rows = list_length
            self.pager_label.set_text('%d - %d (%d) of %d ' % (first_row, last_row, num_rows, list_length))
        except ZeroDivisionError:
            pass

    def log_category_filter_func(self, model, iter, data):
        """Tests if the category in the row is the one in the filter"""
        if not self.current_filter_category:
            return True
        else:
            return model[iter][1] in self.current_filter_category

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
                        self.current_filter_category.append(label)
                        print('%s log type selected!' % label)
                    else:
                        print('%s log type unselected!' % label)
                        if label in self.current_filter_category:
                            self.current_filter_category.remove(label)
        print(self.current_filter_category)
        self.log_category_filter.refilter()
