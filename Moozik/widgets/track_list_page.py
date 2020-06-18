import gi, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gi.repository.GdkPixbuf import Pixbuf
from .listbox_row import *

from ..utils import *

@Gtk.Template(resource_path='/org/gnome/Moozik/ui/track_list_page.ui')
class TrackListPage(Gtk.ScrolledWindow):

    __gtype_name__ = 'track_list_page'

    #TODO rename widgets to album track list
    playlist_album_art = Gtk.Template.Child()
    playlist_album_title = Gtk.Template.Child()
    playlist_artist = Gtk.Template.Child()
    playlist_listview = Gtk.Template.Child()

    #TODO add ability to reorder playlist
    #TODO add ability to save playlist
    #TODO add ability to delete playlist

    def __init__(self, gmusic, player):
        super().__init__()

        self.gmusic = gmusic
        self.player = player
        self.title = ""
        self.now_playing_mode = False
        #self.playlist_listview.set_header_func(Utils().list_header_func, None)
        self.player.connect("player_playlist_updated_signal", self.update_playlist)

    def update_playlist(self, sender, child):
        tracks = self.player.player_get_playlist()
        if self.now_playing_mode:
            self.populate_listview(tracks, self.title, self.now_playing_mode)

    def populate_listview(self, tracks, title, now_playing_mode=False):

        self.title = title
        self.now_playing_mode = now_playing_mode
        for track in self.playlist_listview.get_children():
            self.playlist_listview.remove(track)

        #album_id = tracks[0].get("albumId")
        #album = self.gmusic.get_album(index)

        album_title = 'Unknown'
        subtitle = 'Unknown'
        album_art_list = []

        try:
            subtitle = tracks[0].get("albumArtist")
            album_art_path = tracks[0].get("album_art_path")
        except:
            subtitle = ""
            album_art_path = ""

        for track in tracks:
            if not track.get("albumArtist") == subtitle:
                subtitle = "Various"

            artwork_path = track.get('album_art_path')
            #TODO add album art to tracks - investigate getting multiple album arts or a banner / artist photo?
            # cycle the artist art for each track>=? artistArtRef

            if not any(artwork_path == artwork for artwork in album_art_list):
                if os.path.isfile(artwork_path):
                    album_art_list.append(artwork_path)

        if len(title):
            album_title = title

        if now_playing_mode:
            subtitle = self.get_track_count(len(tracks))

        self.playlist_album_title.set_text(album_title)
        self.playlist_artist.set_text(subtitle)

        if len(album_art_list) > 4:
            #TODO: Join Playlist art together to make a 2x2 grid
            pass
        else:
            if os.path.isfile(album_art_path):
                self.playlist_album_art.set_from_pixbuf(Pixbuf.new_from_file_at_size(album_art_path, 150, 150))

        #TODO sort tracks by album order
        for track in tracks:
            play_list_track = ListboxRow(track, now_playing_mode)
            #play_list_track.load_data(track.get('title'), track.get('artist'))
            play_list_track.connect("play_track_signal", self.player.player_play_single_track)
            play_list_track.connect("add_to_queue_signal", self.player.player_add_to_playlist)
            play_list_track.connect("remove_from_queue_signal", self.player.player_remove_from_playlist)
            play_list_track.connect("play_station_signal", self.player.player_play_radio_station)
            self.playlist_listview.add(play_list_track)

        self.playlist_listview.show_all()

    def get_track_count(self, count):
        if count > 1:
            track_count = '%d tracks' % count
        else:
            track_count = '%d track' % count

        return track_count
