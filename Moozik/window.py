# window.py
#
# Copyright 2018 Dubstar_04
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,_
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi, os
from gi.repository import Gtk, GObject
#GObject.threads_init()
from gi.repository.GdkPixbuf import Pixbuf

#gi.require_version('Handy', '0.0')
#from gi.repository import Handy
import time
from threading import Thread
#from threading import Timer

from .gmusicapi import *
from .player import *
from .settings import *
from .utils import *

from .widgets import ListboxRow, AlbumPlaylistPage, TrackListPage, PlayBarWidget, SearchPage, LoginPage

@Gtk.Template(resource_path='/org/gnome/Moozik/ui/window.ui')
class MoozikWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'MoozikWindow'

    #TODO: change all member variables to _member
    main_stack = Gtk.Template.Child()
    stack_switcher = Gtk.Template.Child()
    back_button = Gtk.Template.Child()
    search_button = Gtk.Template.Child()
    search_bar = Gtk.Template.Child()
    search_entry = Gtk.Template.Child()
    play_widget_revealer = Gtk.Template.Child()

    #menu items
    logout_button = Gtk.Template.Child()
    show_about_dialog_button = Gtk.Template.Child()
    debug_toggle = Gtk.Template.Child()
    about_dialog = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Settings()
        self.gmusic = GmusicAPI()
        self.player = Player(self.gmusic)
        #delete any previous logs and get the log file path
        Utils().create_log_file()

        self.login_page = LoginPage(self.gmusic)

        self.album_page = AlbumPlaylistPage(self.gmusic)
        self.playlist_page = AlbumPlaylistPage(self.gmusic)
        self.main_stack.add_titled(self.album_page, 'album_page', 'Albums')
        self.main_stack.add_titled(self.playlist_page, 'playlists_page', 'Playlists')

        self.now_playing_page = TrackListPage(self.gmusic, self.player)
        self.track_list_page = TrackListPage(self.gmusic, self.player)
        self.search_page = SearchPage(self.gmusic, self.player)

        self.main_stack.add_named(self.login_page, 'login_page')
        self.main_stack.add_named(self.now_playing_page, 'now_playing_page')
        self.main_stack.add_named(self.track_list_page, 'track_list_page')
        self.main_stack.add_named(self.search_page, 'search_page')

        self.play_bar_widget = PlayBarWidget(self.gmusic, self.player, self.play_widget_revealer, self)
        self.play_widget_revealer.add(self.play_bar_widget)

        self.page_breadcrumbs = []

        #connections
        self.gmusic.connect('api_albums_loaded', self.album_page.populate_album_view)
        self.gmusic.connect('api_playlists_loaded', self.playlist_page.populate_album_view)

        self.gmusic.connect('login_request', self.show_login)

        self.play_bar_widget.connect("show_now_playing_signal", self.show_now_playing_page)

        self.login_page.connect("close_login", self.close_login)
        self.login_page.connect("emit_login_code", self.gmusic.handle_login_code)
        self.album_page.connect("album_selected_signal", self.album_selected)
        self.playlist_page.connect("album_selected_signal", self.album_selected)
        self.search_page.connect("album_selected_signal", self.album_selected)

        self.debug_toggle.connect('state-set', self.settings.set_debug)
        self.debug_toggle.set_state(self.settings.get_debug())


        self.load_library()


    def show_login(self, sender):
        self.add_page('login_page')
        self.back_button.set_visible(False)
        self.search_button.set_visible(False)

    def close_login(self, sender, data):
        #self.back_button.set_visible(False)
        self.search_button.set_visible(True)
        self.page_pop()

    def load_library(self):
        init_thread = Thread(target=self.gmusic.load_library, args=())
        init_thread.start()

    @Gtk.Template.Callback()
    def back_button_pressed(self, sender):
        self.page_pop()
        #hide the search bar
        if self.search_bar.get_search_mode():
            self.hide_search()

    @Gtk.Template.Callback()
    def search_button_pressed(self, sender, data):
        Utils().debug(["some text", data])
        current_page = self.add_page('search_page')
        if current_page:
            Utils().debug(['search_page is current page'])
            show_search = not self.search_bar.get_search_mode()
            self.search_bar.set_search_mode(show_search)
        else:
            self.hide_search()

    @Gtk.Template.Callback()
    def init_search(self, sender):
        self.search_text = sender.get_text()
        self.gmusic.search_library(self.search_text)
        self.search_page.load_search_results()

    def hide_search(self):
        self.search_bar.set_search_mode(False)
        self.search_button.set_active(False)
        if self.main_stack.get_visible_child_name() == 'search_page':
            self.page_pop()

    def add_page(self, page_name):
        if self.main_stack.get_visible_child_name() != page_name:
            self.page_breadcrumbs.append(self.main_stack.get_visible_child_name())
            self.stack_switcher.set_visible(False)
            self.back_button.set_visible(True)
            self.hide_search()
            self.main_stack.set_visible_child_name(page_name)
            return True
        else:
            self.page_pop()
            return False

    def page_pop(self):
        Utils().debug([self.page_breadcrumbs])
        if len(self.page_breadcrumbs):
            self.main_stack.set_visible_child_name(self.page_breadcrumbs[-1])
            self.page_breadcrumbs.pop(-1)
            Utils().debug([self.page_breadcrumbs])

        if not len(self.page_breadcrumbs):
            self.stack_switcher.set_visible(True)
            self.back_button.set_visible(False)

    def show_now_playing_page(self, sender, data):
        current_page = self.add_page('now_playing_page')
        if current_page:
            Utils().debug(['now_playing_page is current page'])
            tracks = self.player.player_get_playlist()
            title = "Now Playing"
            self.now_playing_page.populate_listview(tracks, title, now_playing_mode=True)
            #self.now_playing_page.load_current_playlist()

    def album_selected(self, sender, tracks, title):
        self.track_list_page.populate_listview(tracks, title, now_playing_mode=False)
        self.add_page('track_list_page')


    @Gtk.Template.Callback()
    def about_dialog_button_clicked(self, sender):
        Utils().debug(['Show About Dialog'])
        self.about_dialog.show()

    @Gtk.Template.Callback()
    def logout_button_clicked(self, sender):
        Utils().debug(['Logout button clicked'])
        self.gmusic.logout()
        self.show_login(None)






