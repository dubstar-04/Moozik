# window.py
#
# Copyright 2018 Dubstar_04
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk
from .gi_composites import GtkTemplate
from .settings import *
from .gmusicapi import * 

from .albumWidget import *


@GtkTemplate(ui='/org/gnome/Moosic/window.ui')
class MoosicWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'MoosicWindow'

    #set up all the accessible widgets
    username_entry = GtkTemplate.Child()
    password_entry = GtkTemplate.Child()

    album_flowbox = GtkTemplate.Child()
    song_listbox = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        
        self.settings = Settings()
        self.settings.get_settings_obj().bind('username', self.username_entry, 'text', Gio.SettingsBindFlags.DEFAULT)
        self.settings.get_settings_obj().bind('password', self.password_entry, 'text', Gio.SettingsBindFlags.DEFAULT)
        
        self.gmusic = GmusicAPI()

        self.load_library()

    def load_library(self):

        logged_in = self.gmusic.logged_in()

        if logged_in:
            library = self.gmusic.get_library()

            for song in library:
                self.album_flowbox.add(AlbumWidget(song))

        else:
            print('not logged in')

    @GtkTemplate.Callback
    def username_changed(self, sender):
        username =  self.username_entry.get_text()
        print('username changed:', username)
        #self.settings.set_username(username)
        
    @GtkTemplate.Callback
    def password_changed(self, sender):
        password =  self.password_entry.get_text()
        print('password changed:', password)
        #self.settings.set_password(password)
