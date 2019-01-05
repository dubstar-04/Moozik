import gi
from gi.repository import Gtk, GObject
from .gi_composites import GtkTemplate
from gi.repository.GdkPixbuf import Pixbuf
#import os

@Gtk.Template(resource_path='/org/gnome/Moosic/ui/playlist_listbox_row.ui')
class PlaylistRow(Gtk.EventBox):

    __gtype_name__ = 'playlist_listbox_row'

    __gsignals__ = {'play_track_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    list_box_row_track = Gtk.Template.Child()
    list_box_row_artist = Gtk.Template.Child()

    playlist_view_more_button = Gtk.Template.Child()
    playlist_listbox_row_popover = Gtk.Template.Child()

    def __init__(self, track):
        super().__init__()
        #self.init_template()
        #super().__init__()
        #self.init_template()
        self.track = track
        self.load_data()

        self.connect("button-press-event", self.playlist_track_selected)
        self.playlist_view_more_button.connect("clicked", self.playlist_view_more_button_clicked)

    @GtkTemplate.Callback
    def playlist_track_selected(self, sender, child):
        #print('Playlist Track Clicked:', self.track)
        self.emit("play_track_signal", self.track.get('id'))

    @GtkTemplate.Callback
    def playlist_view_more_button_clicked(self, sender):
        print("Playlist More Button Clicked")

    def load_data(self):
        self.list_box_row_track.set_text(self.track.get('title'))
        self.list_box_row_artist.set_text(self.track.get('artist'))



                                              
