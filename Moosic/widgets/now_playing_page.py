import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from .queue_listbox_row import *

from ..utils import *

@Gtk.Template(resource_path='/org/gnome/Moosic/ui/now_playing_page.ui')
class NowPlayingPage(Gtk.EventBox):

    __gtype_name__ = 'now_playing_page'


    now_playing_listview = Gtk.Template.Child()
    now_playing_album_art = Gtk.Template.Child()
    now_playing_playlist_title = Gtk.Template.Child()
    now_playing_track_count = Gtk.Template.Child()

    def __init__(self, gmusic, player):
        super().__init__()

        self.player = player
        self.gmusic = gmusic
        self.now_playing_listview.set_header_func(list_header_func, None)

        self.player.connect("player_playlist_updated_signal", self.update_playlist)

    def update_playlist(self, sender, child):
        self.load_current_playlist()

    def load_current_playlist(self):

        #TODO add ability to reorder
        #TODO add ability to save playlist
        #TODO add ability to delete playlist

        for track in self.now_playing_listview.get_children():
            self.now_playing_listview.remove(track)

        tracks = self.player.player_get_playlist()
        self.set_track_count(len(tracks))
        self.set_playlist_title('Now Playing')

        art_list = []

        for track in tracks:
            #print(track)
            play_list_track = QueueListboxRow(track)
            #TODO player.play_single_track clears the current playlist.
            play_list_track.connect("queue_track_selected_signal", self.player.player_play_queue_track)
            #TODO add to queue makes no sense on the current playlist
            play_list_track.connect("remove_from_queue_signal", self.player.player_remove_from_playlist)
            play_list_track.connect("play_station_signal", self.player.player_play_radio_station)
            play_list_track.connect("reorder_signal", self.player.player_reorder_playlist)
            self.now_playing_listview.add(play_list_track)

            art_list.append(self.gmusic.get_album_art_name(track.get('album')))

        self.set_playlist_art(art_list)

    def set_track_count(self, count):
        if count > 1:
            count_text = '%d tracks' % count
        else:
            count_text = '%d track' % count

        self.now_playing_track_count.set_text(count_text)

    def set_playlist_title(self, playlist_name):
        self.now_playing_playlist_title.set_text(playlist_name)

    def set_playlist_art(self, art_list):

        #TODO add album art to tracks - investigate getting multiple album arts or a banner / artist photo?
        # cycle the artist art for each track>=? artistArtRef

        if art_list:
            playlist_art = art_list[0]

        self.now_playing_album_art.set_from_pixbuf(Pixbuf.new_from_file_at_size(playlist_art, 150, 150))


        
