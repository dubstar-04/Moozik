import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
from .playlist_listbox_row import *
import os

@Gtk.Template(resource_path='/org/gnome/Moosic/ui/now_playing_page.ui')
class NowPlayingPage(Gtk.EventBox):

    __gtype_name__ = 'now_playing_page'


    current_playlist_listview = Gtk.Template.Child()

    def __init__(self, player):
        super().__init__()

        self.player = player

    def load_current_playlist(self):

        #TODO add album art to tracks - investigate getting multiple album arts or a banner / artist photo?
        # cycle the artist art for each track>=? artistArtRef
        #TODO add ability to reorder
        #TODO add ability to save playlist
        #TODO add ability to delete playlist

        for track in self.current_playlist_listview.get_children():
            self.current_playlist_listview.remove(track)

        tracks = self.player.player_get_playlist()

        for track in tracks:
            print(track)
            play_list_track = PlaylistRow(track)
            #TODO player.play_single_track clears the current playlist.
            play_list_track.connect("play_track_signal", self.player.player_play_single_track)
            #TODO add to queue makes no sense on the current playlist
            play_list_track.connect("add_to_queue_signal", self.player.player_add_to_playlist)
            play_list_track.connect("play_station_signal", self.player.player_play_radio_station)
            self.current_playlist_listview.add(play_list_track)


