import gi
from gi.repository import Gtk, GObject
from gi.repository.GdkPixbuf import Pixbuf
#import os

@Gtk.Template(resource_path='/org/gnome/Moosic/ui/playlist_listbox_row.ui')
class PlaylistRow(Gtk.EventBox):

    __gtype_name__ = 'playlist_listbox_row'

    __gsignals__ = {'play_track_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
                    'add_to_queue_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
                    'play_station_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    list_box_row_track = Gtk.Template.Child()
    list_box_row_artist = Gtk.Template.Child()

    playlist_view_more_button = Gtk.Template.Child()
    playlist_listbox_row_popover = Gtk.Template.Child()

    #pop_over_options
    playlist_popover_add_to_queue = Gtk.Template.Child()
    playlist_popover_add_to_playlist = Gtk.Template.Child()
    playlist_popover_start_radio = Gtk.Template.Child()

    def __init__(self, track):
        super().__init__()

        self.track = track
        self.load_data()

    @Gtk.Template.Callback()
    def add_to_queue_clicked(self, sender, child):
        print(sender, child)
        print('Add to Queue clicked:', self.track.get('title'))
        self.playlist_listbox_row_popover.popdown()
        self.emit("add_to_queue_signal", [self.track.get('id')])

    @Gtk.Template.Callback()
    def add_to_playlist_clicked(self, sender, child):
        print('Add to playlist:', self.track.get('title'))
        #self.playlist_listbox_row_popover.popdown()

    @Gtk.Template.Callback
    def start_radio_clicked(self, sender, child):
        print('start radio:', self.track.get('title'))
        self.playlist_listbox_row_popover.popdown()
        self.emit("play_station_signal", [self.track.get('id')])


    @Gtk.Template.Callback()
    def playlist_track_selected(self, sender, child):
        print('Playlist Track Clicked:', self.track)
        self.emit("play_track_signal", self.track.get('id'))

    @Gtk.Template.Callback()
    def playlist_view_more_button_clicked(self, sender):
        print("Playlist More Button Clicked")
        #self.playlist_listbox_row_popover.show_all()
        self.playlist_listbox_row_popover.popup()

    def load_data(self):
        self.list_box_row_track.set_text(self.track.get('title'))
        self.list_box_row_artist.set_text(self.track.get('artist'))



                                              
