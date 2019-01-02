import gi
from gi.repository import Gdk, GObject, Gtk

@Gtk.Template(resource_path='/org/gnome/Moosic/SongWidget.ui')
class AlbumWidget(Gtk.EventBox):

    __gtype_name__ = 'AlbumWidget'

    __gsignals__ = { }

    AlbumArt_Image = Gtk.Template.Child()
    AlbumTitle_Label = Gtk.Template.Child()
    
    def __init__(self, media):
        super().__init__()

        self._media = media

