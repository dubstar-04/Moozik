import gi, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
from .listbox_row import *

from ..utils import *

@Gtk.Template(resource_path='/org/gnome/Moosic/ui/track_list_page.ui')
class TrackListPage(Gtk.ScrolledWindow):

    __gtype_name__ = 'track_list_page'

    #TODO rename widgets to album track list
    playlist_album_art = Gtk.Template.Child()
    playlist_album_title = Gtk.Template.Child()
    playlist_artist = Gtk.Template.Child()
    playlist_listview = Gtk.Template.Child()

    def __init__(self, gmusic, player):
        super().__init__()

        self.gmusic = gmusic
        self.player = player
        self.playlist_listview.set_header_func(list_header_func, None)

    def populate_listview(self, index):

        for track in self.playlist_listview.get_children():
            self.playlist_listview.remove(track)

        album = self.gmusic.get_album(index)

        album_title = album.get("title")
        artist = album.get("artist")
        album_art_path = album.get("album_art_path")

        self.playlist_album_title.set_text(album_title)
        self.playlist_artist.set_text(artist)
        self.playlist_album_art.set_from_pixbuf(Pixbuf.new_from_file_at_size(album_art_path, 150, 150))

        tracks = self.gmusic.get_album_tracks(index)

        #TODO sort tracks by album order
        for track in tracks:
            play_list_track = ListboxRow(track)
            play_list_track.load_data(track.get('title'), track.get('artist'))
            play_list_track.connect("play_track_signal", self.player.player_play_single_track)
            play_list_track.connect("add_to_queue_signal", self.player.player_add_to_playlist)
            play_list_track.connect("play_station_signal", self.player.player_play_radio_station)
            self.playlist_listview.add(play_list_track)
