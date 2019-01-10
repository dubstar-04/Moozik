import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

import webbrowser

@Gtk.Template(resource_path='/org/gnome/Moosic/ui/login_dialog.ui')
class LoginDialog(Gtk.Dialog):

    code_entry = Gtk.Template.Child()

    __gtype_name__ = 'login_dialog'

    def __init__(self, url):
        super().__init__()

        self.url = url
        self.code = ""

    @Gtk.Template.Callback()
    def get_key(self, sender):
        webbrowser.open(self.url)

    @Gtk.Template.Callback()
    def apply_clicked(self, sender):
        print(self.code_entry.get_text())
        self.code = self.code_entry.get_text()
        self.close()

    @Gtk.Template.Callback()
    def cancel_dialog(self,sender):
        self.close()

    @Gtk.Template.Callback()
    def on_response(self, sender, response):
        print('response')

    def get_code(self):
        return self.code
        
