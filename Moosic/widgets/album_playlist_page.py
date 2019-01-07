import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from gi.repository.GdkPixbuf import Pixbuf

from .albumWidget import *

import os

@Gtk.Template(resource_path='/org/gnome/Moosic/ui/album_playlist_page.ui')
class AlbumPlaylistPage(Gtk.ScrolledWindow):

    __gtype_name__ = 'album_playlist_page'

    __gsignals__ = {'album_selected_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_INT,)) }

    album_flowbox = Gtk.Template.Child()

    def __init__(self, albums):
        super().__init__()

        self.albums = albums
        self.populate_album_view()

    def populate_album_view(self):
        for album in self.albums:
            self.album_flowbox.add(AlbumWidget(album))

    @Gtk.Template.Callback()
    def album_selected(self, sender, child):
        #print('album clicked:', sender, child)
        print('album_playlist_page:', child.get_index())
        self.emit("album_selected_signal", child.get_index())





