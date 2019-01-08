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

import gi, os
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf

from .gmusicapi import *
from .player import *
from .settings import *

from .widgets import PlaylistRow, NowPlayingPage, AlbumPlaylistPage, TrackListPage, PlayBarWidget

@Gtk.Template(resource_path='/org/gnome/Moosic/ui/window.ui')
class MoosicWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'MoosicWindow'

    #set up all the accessible widgets
    username_entry = Gtk.Template.Child()
    password_entry = Gtk.Template.Child()

    main_stack = Gtk.Template.Child()
    #album_playlist_stack = Gtk.Template.Child()
    stack_switcher = Gtk.Template.Child()
    back_button = Gtk.Template.Child()
    play_widget_revealer = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Settings()
        #TODO move settings to own ui
        self.settings.get_settings_obj().bind('username', self.username_entry, 'text', Gio.SettingsBindFlags.DEFAULT)
        self.settings.get_settings_obj().bind('password', self.password_entry, 'text', Gio.SettingsBindFlags.DEFAULT)

        self.gmusic = GmusicAPI()
        self.player = Player(self.gmusic)
        self.load_library()


        self.album_page = AlbumPlaylistPage(self.gmusic.get_albums())
        self.playlist_page = AlbumPlaylistPage(self.gmusic.get_albums())

        self.album_page.connect("album_selected_signal", self.album_selected)
        self.playlist_page.connect("album_selected_signal", self.album_selected)

        self.main_stack.add_titled(self.album_page, 'album_page', 'Albums')
        self.main_stack.add_titled(self.playlist_page, 'playlists_page', 'Playlists')

        self.now_playing_page = NowPlayingPage(self.player)
        self.track_list_page = TrackListPage(self.gmusic, self.player)

        self.main_stack.add_named(self.now_playing_page, 'now_playing_page')
        self.main_stack.add_named(self.track_list_page, 'track_list_page')

        self.play_bar_widget = PlayBarWidget(self.gmusic, self.player, self.play_widget_revealer)
        self.play_bar_widget.connect("show_now_playing_signal", self.show_now_playing_page)

        self.play_widget_revealer.add(self.play_bar_widget)

        self.page_breadcrumbs = []

    #TODO move this to init of the gmusic object
    def load_library(self):
        logged_in = self.gmusic.logged_in()

        if logged_in:
            print('logged in')
        else:
            print('not logged in')

    @Gtk.Template.Callback()
    def back_button_pressed(self, sender):
        self.page_pop()

    def page_pop(self):
        print(self.page_breadcrumbs)
        if len(self.page_breadcrumbs):
            self.main_stack.set_visible_child_name(self.page_breadcrumbs[-1])
            self.page_breadcrumbs.pop(-1)
            print(self.page_breadcrumbs)

        if not len(self.page_breadcrumbs):
            self.stack_switcher.set_visible(True)
            self.back_button.set_visible(False)

    def show_now_playing_page(self, sender, data):
        if self.main_stack.get_visible_child_name() != 'now_playing_page':
            self.page_breadcrumbs.append(self.main_stack.get_visible_child_name())
            self.stack_switcher.set_visible(False)
            self.back_button.set_visible(True)
            self.now_playing_page.load_current_playlist()
            self.main_stack.set_visible_child_name('now_playing_page')
        else:
            self.page_pop()

    @Gtk.Template.Callback()
    def album_selected(self, sender, index):
        self.page_breadcrumbs.append(self.main_stack.get_visible_child_name())
        self.track_list_page.populate_listview(index)
        self.main_stack.set_visible_child_name('track_list_page')
        self.stack_switcher.set_visible(False)
        self.back_button.set_visible(True)


    #TODO move settings to its own class
    @Gtk.Template.Callback()
    def username_changed(self, sender):
        username =  self.username_entry.get_text()
        print('username changed:', username)
        #self.settings.set_username(username)

    @Gtk.Template.Callback()
    def password_changed(self, sender):
        password =  self.password_entry.get_text()
        print('password changed:', password)
        #self.settings.set_password(password)


        
