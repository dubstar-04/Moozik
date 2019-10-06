import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from gi.repository.GdkPixbuf import Pixbuf
from ..utils import *

from .albumWidget import *

@Gtk.Template(resource_path='/org/gnome/Moozik/ui/album_playlist_page.ui')
class AlbumPlaylistPage(Gtk.ScrolledWindow):

    __gtype_name__ = 'album_playlist_page'

    __gsignals__ = {'album_selected_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,GObject.TYPE_PYOBJECT)) }

    album_flowbox = Gtk.Template.Child()
    album_playlist_loading_spiner = Gtk.Template.Child()
    album_playlist_loading = Gtk.Template.Child()
    no_network_box = Gtk.Template.Child()

    def __init__(self, gmusic):

        super().__init__()

        self.gmusic = gmusic
        self.show_loading()

        self.gmusic.connect('waiting_for_network', self.waiting_for_network)

    def waiting_for_network(self, sender, waiting):
        Utils().debug(['waiting:', waiting])
        if waiting:
            self.show_loading('waiting')
        else:
            self.show_loading()

    def show_loading(self, state='loading'):

        Utils().debug(['show_loading', state])

        if state == 'waiting':
            self.album_flowbox.set_visible(False)
            self.no_network_box.set_visible(True)
            self.album_playlist_loading.set_visible(False)
            self.album_playlist_loading_spiner.stop()
        if state == 'loading':
            self.album_flowbox.set_visible(False)
            self.no_network_box.set_visible(False)
            self.album_playlist_loading.set_visible(True)
            self.album_playlist_loading_spiner.start()
        if state == 'loaded':
            self.album_flowbox.set_visible(True)
            self.no_network_box.set_visible(False)
            self.album_playlist_loading.set_visible(False)
            self.album_playlist_loading_spiner.stop()



    def populate_album_view(self, sender, child, album_data):
        Utils().debug(['Album page: Load Albums'])
        self.show_loading('loaded')
        albums = album_data #self.gmusic.get_albums()
        for album in albums:
            GObject.idle_add(self.album_flowbox.add, AlbumWidget(album))

    @Gtk.Template.Callback()
    def album_selected(self, sender, child):
        #Utils().debug(['album clicked:', sender, child])
        Utils().debug(['album_playlist_page - Child Index:', child.get_index()])

        kind = child.get_children()[0].get_kind()
        title = child.get_children()[0].get_title()
        tracks = self.gmusic.get_album_tracks(child.get_index(), kind)

        self.emit("album_selected_signal", tracks, title)
