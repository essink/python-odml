import gtk

class TreeView(object):
    """
    Covers basic tasks of Treeview objects
    """
    popup = None

    def __init__(self, store=None):
        tv = gtk.TreeView(store)
        tv.set_headers_visible(False)

        renderer = gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.connect("edited", self.on_edited, None)

        if self.on_selection_change is not None:
            selection = tv.get_selection()
            selection.set_mode(gtk.SELECTION_BROWSE)
            selection.connect("changed", self.on_selection_change)

        if self.on_button_press is not None:
            tv.connect("button_press_event", self.on_button_press)

        tv.set_headers_visible(True)
        tv.set_rules_hint(True)

        self._treeview = tv

    def add_column(self, name, edit_func=None, id=0, data=0):
        renderer = gtk.CellRendererText()
        if edit_func:
            renderer.set_property("editable", True)
            renderer.connect("edited", edit_func, data)

        column = gtk.TreeViewColumn(name, renderer, text=id)
        self._treeview.append_column(column)
        return column

    def on_button_press(self, widget, event):
        if event.button == 3: # right-click
            x = int(event.x)
            y = int(event.y)
            model = widget.get_model()
            path = widget.get_path_at_pos(x, y)
            obj = None

            if path:
                path, col, x, y = path
            else:
                path = ()

            if path:
                obj = model.on_get_iter(path)._obj

            if self.popup is None:
                return

            self.popup_data = (model, path, obj)
            self.popup.popup(None, None, None, event.button, event.time)

    def on_edited(self, widget, path, new_value, data):
        """
        a user edited a value

        now callback another method with more meaningful information
        """
        model = self._treeview.get_model()
        gtk_tree_iter = model.get_iter(path)
        tree_iter = model.on_get_iter(model.get_path(gtk_tree_iter))
        return self.on_object_edit(tree_iter, data, new_value)

    def execute(self, cmd):
        cmd()

    on_selection_change = None
