import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from gi.repository.GdkPixbuf import Pixbuf

from .albumWidget import *

@Gtk.Template(resource_path='/org/gnome/Moosic/ui/album_playlist_page.ui')
class AlbumPlaylistPage(Gtk.ScrolledWindow):

    __gtype_name__ = 'album_playlist_page'

    __gsignals__ = {'album_selected_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)) }

    album_flowbox = Gtk.Template.Child()
    album_playlist_loading_spiner = Gtk.Template.Child()

    def __init__(self, gmusic):
        super().__init__()

        self.gmusic = gmusic

        self.show_loading(True)


    def show_loading(self, state):
        if state:
            self.album_flowbox.visible = False
            self.album_playlist_loading_spiner.visible = True
            self.album_playlist_loading_spiner.start()
        else:
            self.album_flowbox.visible = True
            self.album_playlist_loading_spiner.visible = False
            self.album_playlist_loading_spiner.stop()

    def populate_album_view(self, sender, child):
        print('Album page: Load Albums')
        self.show_loading(False)
        albums = self.gmusic.get_albums()
        for album in albums:
            GObject.idle_add(self.album_flowbox.add, AlbumWidget(album))

    @Gtk.Template.Callback()
    def album_selected(self, sender, child):
        #print('album clicked:', sender, child)
        print('album_playlist_page:', child.get_index())

        tracks = self.gmusic.get_album_tracks(child.get_index())

        self.emit("album_selected_signal", tracks)
