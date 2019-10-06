import gi, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
from ..utils import *

@Gtk.Template(resource_path='/org/gnome/Moozik/ui/albumWidget.ui')
class AlbumWidget(Gtk.EventBox):

    __gtype_name__ = 'albumWidget'

    #__gsignals__ = {'album_selected_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_STRING,)) }

    AlbumArt_Image = Gtk.Template.Child()
    AlbumTitle_Label = Gtk.Template.Child()
    Artist_Label = Gtk.Template.Child()

    def __init__(self, album):
        super().__init__()

        self.album = album
        self.load_data()

    def load_data(self):

        album = self.album
        album_title = album.get("title")
        artist = album.get("artist")
        album_art_path = album.get("album_art_path")

        if os.path.isfile(album_art_path):
            self.AlbumArt_Image.set_from_pixbuf(Pixbuf.new_from_file_at_size(album_art_path, 150, 150))

        self.AlbumTitle_Label.set_text(album_title)
        self.Artist_Label.set_text(artist)

    def get_title(self):
        return self.album.get('title')

    def get_kind(self):
        return self.album.get('kind')

    def album_selected(self, sender, child):
        Utils().debug('album_widget_pressed:')
        #self.emit("album_selected_signal", [self.track.get('id')])
