import os, gi, cairo
from gi.repository import Gtk, GObject, Gdk
gi.require_version('Handy', '1')
from gi.repository import Handy
from gi.repository.GdkPixbuf import Pixbuf
from ..utils import *

@Gtk.Template(resource_path='/org/gnome/Moozik/ui/listbox_row.ui')
class ListboxRow(Handy.ActionRow):

    __gtype_name__ = 'listbox_row'

    __gsignals__ = {#'queue_track_selected_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (int,)),
                     'remove_from_queue_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (int,)),
                     'reorder_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
                     'play_track_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
                     'add_to_queue_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
                     'play_station_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    #TODO Add the track length in time
    #listbox_row_popover = Gtk.Template.Child()
    #row_drag_handle = Gtk.Template.Child()

    def __init__(self, track, DnD=False, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.track = track
        self.title = self.track.get('title')
        self.subtitle = self.track.get('artist')

        self.set_title(self.title)
        self.set_subtitle(self.subtitle)

        ## work around handyactionrow not been supported in glade

        self.more_menu = Gtk.Button()
        self.menu_image = Gtk.Image()
        self.menu_image.set_from_icon_name('view-more-symbolic', Gtk.IconSize.BUTTON)#
        builder = Gtk.Builder()
        self.more_menu.add_child(builder, self.menu_image)
        self.more_menu.connect('clicked', self.show_popup_menu)
        menu_style_context = self.more_menu.get_style_context()
        menu_style_context.add_class("flat")

        self.add_child(builder, self.more_menu)
        self.set_activatable(True)
        self.connect("activated", self.playlist_track_selected)

        self.popover = Gtk.Popover()



        #only show the drag handle if drag and drop is being used
        #self.row_drag_handle.set_visible(DnD)
        if DnD:
            self.set_icon_name('open-menu-symbolic')

        #Drag and Drop
        #target = Gtk.TargetEntry.new('Gtk.ListBoxRow', Gtk.TargetFlags(1), 129)

        #source
        #self.row_drag_handle.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [target], Gdk.DragAction.MOVE);
        #self.row_drag_handle.connect("drag-data-get", self.on_drag_data_get)
        #self.row_drag_handle.connect("drag-begin", self.on_drag_begin)

        #destination
        #self.drag_dest_set(Gtk.DestDefaults.ALL, [target], Gdk.DragAction.MOVE)
        #self.connect("drag-data-received", self.on_drag_data_received)

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

    #@Gtk.Template.Callback()
    def add_to_queue_clicked(self, sender, child):
        self.emit("add_to_queue_signal", [self.track])
        self.popover.popdown()

 #   @Gtk.Template.Callback()
 #   def remove_from_queue_clicked(self, sender, child):
 #       Utils().debug([sender, child])
 #       Utils().debug(['Remove From Queue clicked - Index:', self.get_parent().get_index()])
 #       self.listbox_row_popover.popdown()
 #       self.emit("remove_from_queue_signal", self.get_parent().get_index())

 #    @Gtk.Template.Callback()
 #    def add_to_playlist_clicked(self, sender, child):
 #        Utils().debug(['Add to playlist:', self.track])
        #self.listbox_row_popover.popdown()

 #    @Gtk.Template.Callback()
    def start_radio_clicked(self, sender, child):
        Utils().debug(['start radio:', self.track.get('title')])
        self.popover.popdown()
        self.emit("play_station_signal", [self.track.get('id')])


    #@Gtk.Template.Callback()
    def playlist_track_selected(self, sender):
        Utils().debug(['Track Clicked:', self.track])
        #self.emit("queue_track_selected_signal", self.get_parent().get_index())
        self.emit("play_track_signal", self.track)

    def show_popup_menu(self, sender):
        Utils().debug(['Show More Menu:', self.track])
        #popover = PlayListPopover()


        menu_item_1 = Gtk.EventBox()
        menu_item_1.add(Gtk.Label("Add To Queue"))
        menu_item_1.connect("button-press-event", self.add_to_queue_clicked)

        menu_item_2 = Gtk.EventBox()
        menu_item_2.add(Gtk.Label("Start Radio"))
        menu_item_2.connect("button-press-event", self.start_radio_clicked)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.pack_start(menu_item_1, False, True, 10)
        vbox.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, True, 10)
        vbox.pack_start(menu_item_2, False, True, 10)

        self.popover.add(vbox)
        self.popover.set_position(Gtk.PositionType.BOTTOM)
        self.popover.set_relative_to(sender)
        self.popover.show_all()
        self.popover.popup()

    # def load_album_art(self, album_art_path):

        #album_art_path = album.get("album_art_path")

    #     self.list_box_row_album_art.set_visible(True)

    #     if os.path.isfile(album_art_path):
    #         self.list_box_row_album_art.set_from_pixbuf(Pixbuf.new_from_file_at_size(album_art_path, 40, 40))
