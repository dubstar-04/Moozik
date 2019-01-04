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

import gi
from gi.repository import Gtk
#gi.require_version('Handy', '0.0')
#from gi.repository import Handy
from .gi_composites import GtkTemplate
from .settings import *
from .gmusicapi import * 

from .albumWidget import *
from .playlist_listbox_row import *

import os


@GtkTemplate(ui='/org/gnome/Moosic/ui/window.ui')
class MoosicWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'MoosicWindow'

    #set up all the accessible widgets
    username_entry = GtkTemplate.Child()
    password_entry = GtkTemplate.Child()

    album_flowbox = GtkTemplate.Child()
    playlist_flowbox = GtkTemplate.Child()
    window_stack = GtkTemplate.Child()
    main_stack = GtkTemplate.Child()
    stack_switcher = GtkTemplate.Child()
    back_button = GtkTemplate.Child()

    #current playlist page
    playlist_album_art = GtkTemplate.Child()
    playlist_album_title = GtkTemplate.Child()
    playlist_artist = GtkTemplate.Child()
    playlist_listview = GtkTemplate.Child()
    #current_playlist_store = Gtk.ListStore(int, str, str, str)

    #playbar
    play_widget_revealer = GtkTemplate.Child()
    #self.play_widget_revealer.set_reveal_child(False)

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
            albums = self.gmusic.get_albums()

            #count = 0
            for album in albums:
                #print('Album in window:', album)
                #if count < 20:
                self.album_flowbox.add(AlbumWidget(album))
                #count = count + 1

        else:
            print('not logged in')

    @GtkTemplate.Callback
    def back_button_pressed(self, sender):
        self.stack_switcher.set_visible(True)
        self.back_button.set_visible(False)
        self.main_stack.set_visible_child_name('main_stack_page_1')


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

    @GtkTemplate.Callback
    def album_selected(self, sender, child):
        #print('album clicked:', sender, child)
        #print('album:', child.get_index())

        #print('visible child:', self.window_stack.get_visible_child_name())
        self.main_stack.set_visible_child_name('main_stack_page_2')
        self.stack_switcher.set_visible(False)
        self.back_button.set_visible(True)

        album = self.gmusic.get_album(child.get_index())

        album_title = album.get("title")
        artist = album.get("artist")
        album_art_path = album.get("album_art_path")

        self.playlist_album_title.set_text(album_title)
        self.playlist_artist.set_text(artist)
        self.playlist_album_art.set_from_pixbuf(Pixbuf.new_from_file_at_size(album_art_path, 150, 150))

        tracks = self.gmusic.get_album_tracks(child.get_index())

        for track in tracks:
            self.playlist_listview.add(PlaylistRow(track))
