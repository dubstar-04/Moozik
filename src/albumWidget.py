from gi.repository import Gtk
from .gi_composites import GtkTemplate

@Gtk.Template(resource_path='/org/gnome/Moosic/albumWidget.ui')
class AlbumWidget(Gtk.EventBox):

    __gtype_name__ = 'albumWidget'

    __gsignals__ = { }

    AlbumArt_Image = Gtk.Template.Child()
    AlbumTitle_Label = Gtk.Template.Child()
    
    def __init__(self, media):
        super().__init__()

        self._media = media
        self.load_data()

    def load_data(self):

        song = self._media
        #print(song)
        album_title = song.get("album")
        artist = song.get("artist")
        track_title = song.get("title")
        #TODO Should we always used the first album art?
        album_art = ''
        try:
            album_art = song.get("albumArtRef")[0].get("url")
        except Exception:
            print('no album art available')

        #print(artist, album_title, track_title, album_art)

        #self.AlbumArt_Image = album_art
        self.AlbumTitle_Label.set_text(album_title)

