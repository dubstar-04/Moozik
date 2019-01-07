import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def list_header_func(row, before, user_data):
    if before and not row.get_header():
        row.set_header(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))
