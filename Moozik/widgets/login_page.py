import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from ..utils import *

import webbrowser

@Gtk.Template(resource_path='/org/gnome/Moozik/ui/login_page.ui')
class LoginPage(Gtk.EventBox):

    code_entry = Gtk.Template.Child()
    apply_button = Gtk.Template.Child()

    __gtype_name__ = 'login_page'

    __gsignals__ = {'close_login' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (bool, )),
                    'emit_login_code' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))
                    }

    def __init__(self):
        super().__init__()

        self.url = ""
        self.code = ""
        #self.apply_button.set_visible(False)

    def set_url(self, url):
        self.url = url

    @Gtk.Template.Callback()
    def get_key(self, sender):
        webbrowser.open(self.url)

    @Gtk.Template.Callback()
    def key_changed(self, sender):
        if len(self.code_entry.get_text()):
            self.apply_button.set_visible(True)

    @Gtk.Template.Callback()
    def apply_clicked(self, sender):
        Utils().debug([self.code_entry.get_text()])
        self.code = self.code_entry.get_text()
        self.emit('emit_login_code', self.code)
        self.close()

    def close(self):
        self.emit('close_login', True)

        
