import gi, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from ..utils import *

@Gtk.Template(resource_path='/org/gnome/Moozik/ui/cast_dialog.ui')
class CastDialog(Gtk.Dialog):

    __gtype_name__ = 'cast_dialog'
    #__gsignals__ = {'device_selected' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ()) }

    stop_casting_button = Gtk.Template.Child()
    device_list = Gtk.Template.Child()
    cancel_button = Gtk.Template.Child()

    cast_dialog_header = Gtk.Template.Child()

    def __init__(self, parent):
        super().__init__()

        self.props.transient_for = parent
        self.set_titlebar(self.cast_dialog_header)

    #def __init__(self):
    #    super().__init__()

        self.devices = []


    def show_devices(self):

        self.clear_device_list()

        for device in self.devices:
            print('In Dialog - Device:', device )
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            row.add(hbox)
            label = Gtk.Label(str(device), xalign=0)
            hbox.pack_start(label, True, True, 0)
            self.device_list.add(row)

        self.show_all()

    def clear_device_list(self):
        for device in self.device_list.get_children():
            self.device_list.remove(device)

    def set_devices(self, devices):
        self.devices = devices
        self.show_devices()

    @Gtk.Template.Callback()
    def cancel_button_clicked(self, sender):
        print('close dialog')
        #self.response(Gtk.ResponseType.REJECT)
        self.hide()

    @Gtk.Template.Callback()
    def stop_casting_clicked(self, sender):
        print('stop casting')
