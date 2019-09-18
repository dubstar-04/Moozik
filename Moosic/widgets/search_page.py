import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from .listbox_row import *

from ..utils import *

@Gtk.Template(resource_path='/org/gnome/Moosic/ui/search_page.ui')
class SearchPage(Gtk.EventBox):

    __gtype_name__ = 'search_page'


    search_listview = Gtk.Template.Child()
    search_page_placeholder = Gtk.Template.Child()

    def __init__(self, gmusic, player):
        super().__init__()

        self.player = player
        self.gmusic = gmusic

    def load_search_results(self):

        for entry in self.search_listview.get_children():
            self.search_listview.remove(entry)

        search_results = self.gmusic.get_search_results()

        if not search_results:
            self.search_page_placeholder.set_visible(True)

        if search_results:
            self.search_page_placeholder.set_visible(False)

            for item in search_results:

                subtitle = '{0} by {1}'.format(item.get('source_type'), item.get('artist'))
                search_result = ListboxRow(item)

                search_result.connect("play_track_signal", self.player.player_play_single_track)
                search_result.connect("add_to_queue_signal", self.player.player_add_to_playlist)
                search_result.connect("play_station_signal", self.player.player_play_radio_station)

                search_result.load_data(item.get('title'), subtitle)
                search_result.load_album_art(item.get('album_art_path'))
                self.search_listview.add(search_result)
