import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from .listbox_row import *

from ..utils import *

@Gtk.Template(resource_path='/org/gnome/Moosic/ui/search_page.ui')
class SearchPage(Gtk.EventBox):

    __gtype_name__ = 'search_page'

    __gsignals__ = {'album_selected_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,GObject.TYPE_PYOBJECT)) }

    search_listview = Gtk.Template.Child()
    search_page_placeholder = Gtk.Template.Child()

    def __init__(self, gmusic, player):
        super().__init__()

        self.player = player
        self.gmusic = gmusic

        self.gmusic.connect('album_art_updated', self.update_album_art)

    def update_album_art(self, sender, data):
        #print('search_page: update album art', sender, data)
        self.load_search_results()

    def item_selected(self, sender, item):

        if item.get('kind') == 'sj#track':
            self.player.player_play_single_track
            #TODO: handle playing a single playlist track
            self.player.player_play_single_track(sender, item)

        if item.get('kind') == 'sj#album':
            #print('item_selected:', sender, item)
            tracks = self.gmusic.get_album_info(item.get('album_id'))
            title = item.get("title")
            self.emit("album_selected_signal", tracks, title)


    def load_search_results(self):

        for entry in self.search_listview.get_children():
            self.search_listview.remove(entry)

        search_results = self.gmusic.get_search_results()

        if not search_results:
            self.search_page_placeholder.set_visible(True)

        if search_results:
            self.search_page_placeholder.set_visible(False)

            for item in search_results:

                kind = item.get('kind').replace('sj#','').title()
                subtitle = '{0} by {1}'.format(kind, item.get('artist'))
                search_result = ListboxRow(item)

                search_result.connect("play_track_signal", self.item_selected)
                search_result.connect("add_to_queue_signal", self.player.player_add_to_playlist)
                search_result.connect("play_station_signal", self.player.player_play_radio_station)

                search_result.load_data(item.get('title'), subtitle)
                search_result.load_album_art(item.get('album_art_path'))
                self.search_listview.add(search_result)
        
