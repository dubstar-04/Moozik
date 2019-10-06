import os, gi, cairo
from gi.repository import Gtk, GObject, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from ..utils import *

@Gtk.Template(resource_path='/org/gnome/Moosic/ui/listbox_row.ui')
class ListboxRow(Gtk.EventBox):

    __gtype_name__ = 'listbox_row'

    __gsignals__ = {#'queue_track_selected_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (int,)),
                    'remove_from_queue_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (int,)),
                    'reorder_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
                    'play_track_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
                    'add_to_queue_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
                    'play_station_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    list_box_row_track = Gtk.Template.Child()
    list_box_row_artist = Gtk.Template.Child()
    list_box_row_album_art = Gtk.Template.Child()

    #TODO Add the track length in time
    listbox_row_popover = Gtk.Template.Child()
    row_drag_handle = Gtk.Template.Child()

    def __init__(self, track, DnD=False):
        super().__init__()

        self.track = track
        #self.load_data()

        #only show the drag handle if drag and drop is being used
        self.row_drag_handle.set_visible(DnD)

        #Drag and Drop
        target = Gtk.TargetEntry.new('Gtk.ListBoxRow', Gtk.TargetFlags(1), 129)

        #source
        self.row_drag_handle.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [target], Gdk.DragAction.MOVE);
        self.row_drag_handle.connect("drag-data-get", self.on_drag_data_get)
        self.row_drag_handle.connect("drag-begin", self.on_drag_begin)

        #destination
        self.drag_dest_set(Gtk.DestDefaults.ALL, [target], Gdk.DragAction.MOVE)
        self.connect("drag-data-received", self.on_drag_data_received)


    def on_drag_begin(self, widget, drag_context):
        Utils().debug(['drag-begin'])
        #Utils().debug(['widget:', widget, 'drag_context:', drag_context])
        listbox_row = self.get_parent()
        Utils().debug(['listbox_row:', listbox_row])
        allocation = listbox_row.get_allocation()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, allocation.width, allocation.height)
        cr = cairo.Context(surface)
        #context = listbox_row.get_style_context()
        #context.add_class("drag-icon")
        listbox_row.draw(cr)
        Gtk.drag_set_icon_surface(drag_context, surface)
        #Gtk.StyleContext.remove_class (context, "drag-icon")

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        Utils().debug(['drag-data-get'])
        index = self.get_parent().get_index()
        data.set(Gdk.Atom.intern_static_string('Gtk.ListBoxRow'), 32, [index])

    def on_drag_data_received(self, widget, drag_context, x,y, data,info, time):
        Utils().debug(['drag-data-received'])
        source_index = data.get_data()[0]
        target_index = widget.get_parent().get_index()
        Utils().debug(['source_index:', source_index, 'target_index:', target_index])
        self.emit("reorder_signal", [source_index, target_index])

    @Gtk.Template.Callback()
    def add_to_queue_clicked(self, sender, child):
        self.emit("add_to_queue_signal", [self.track])
        self.listbox_row_popover.popdown()

 #   @Gtk.Template.Callback()
 #   def remove_from_queue_clicked(self, sender, child):
 #       Utils().debug([sender, child])
 #       Utils().debug(['Remove From Queue clicked - Index:', self.get_parent().get_index()])
 #       self.listbox_row_popover.popdown()
 #       self.emit("remove_from_queue_signal", self.get_parent().get_index())

    @Gtk.Template.Callback()
    def add_to_playlist_clicked(self, sender, child):
        Utils().debug(['Add to playlist:', self.track])
        #self.listbox_row_popover.popdown()

    @Gtk.Template.Callback()
    def start_radio_clicked(self, sender, child):
        Utils().debug(['start radio:', self.track.get('title')])
        self.listbox_row_popover.popdown()
        self.emit("play_station_signal", [self.track.get('id')])


    @Gtk.Template.Callback()
    def playlist_track_selected(self, sender, child):
        Utils().debug(['Track Clicked:', self.track])
        #self.emit("queue_track_selected_signal", self.get_parent().get_index())
        self.emit("play_track_signal", self.track)

    @Gtk.Template.Callback()
    def playlist_view_more_clicked(self, sender, child):
        Utils().debug(["Playlist More Clicked"])
        self.listbox_row_popover.popup()

    def load_data(self, title, subtitle):
        self.list_box_row_track.set_text(title)
        self.list_box_row_artist.set_text(subtitle)

    def load_album_art(self, album_art_path):

        #album_art_path = album.get("album_art_path")

        self.list_box_row_album_art.set_visible(True)

        if os.path.isfile(album_art_path):
            self.list_box_row_album_art.set_from_pixbuf(Pixbuf.new_from_file_at_size(album_art_path, 40, 40))
