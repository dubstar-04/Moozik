import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from gi.repository.GdkPixbuf import Pixbuf

@Gtk.Template(resource_path='/org/gnome/Moosic/ui/play_bar_widget.ui')
class PlayBarWidget(Gtk.ActionBar):

    __gtype_name__ = 'play_bar_widget'
    __gsignals__ = {'show_now_playing_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,)) }

    play_widget_track_title = Gtk.Template.Child()
    playwidget_artist = Gtk.Template.Child()
    play_widget_progress_duration = Gtk.Template.Child()
    playwidget_slider = Gtk.Template.Child()
    play_widget_show_playlist = Gtk.Template.Child()
    play_widget_album_art = Gtk.Template.Child()
    play_widget_play_pause_button = Gtk.Template.Child()
    play_pause_btn_image = Gtk.Template.Child()

    def __init__(self, gmusic, player, revealer):
        super().__init__()

        self.gmusic = gmusic
        self.player = player
        self.play_widget_revealer = revealer
        self.player.connect("player_state_change_signal", self.handle_player_states)
        self.player.connect("player_progress_change_signal", self.playbar_widget_slider_update)
        self.playwidget_slider_handler_id = self.playwidget_slider.connect("value-changed", self.track_seek)

    def handle_player_states(self, sender, state):
        print('update_play_bar:', sender, state)
        player_state = self.player.player_get_state().value
        print('player state:', player_state)

        if player_state == 1:
            print('player is stopped')
            self.player_stopped_state()
        elif player_state == 2:
            print('player is playing')
            self.player_playing_state()
        elif player_state == 3:
            print('player is paused')
            self.player_paused_state()

    def player_stopped_state(self):
        self.play_widget_revealer.set_reveal_child(False)

    def player_playing_state(self):
        self.play_pause_btn_image.set_from_icon_name('media-playback-pause-symbolic', Gtk.IconSize.BUTTON)

        track = self.player.player_get_playing_track()
        self.play_widget_track_title.set_text(track.get('title'))
        self.playwidget_artist.set_text(track.get('artist'))
        album_art_path = self.gmusic.get_album_art_name(track.get('album'))
        #TODO what is the correct artwork size?
        #TODO redesign the playbar so the progress bar is full width
        self.play_widget_album_art.set_from_pixbuf(Pixbuf.new_from_file_at_size(album_art_path, 30, 30))
        self.play_widget_revealer.set_reveal_child(True)

    @Gtk.Template.Callback()
    def play_pause(self, widget):
        player_state = self.player.player_get_state().value
        if player_state == 1:
            print('player is stopped')
            self.player.player_play()
        elif player_state == 2:
            print('player is playing')
            self.player.player_pause()
        elif player_state == 3:
            print('player is paused')
            self.player.player_play()

    def track_seek(self, widget):
        self.player.player_seek(self.playwidget_slider.get_value())

    def player_paused_state(self):
         self.play_pause_btn_image.set_from_icon_name('media-playback-start-symbolic', Gtk.IconSize.BUTTON)

    @Gtk.Template.Callback()
    def play_widget_show_playlist(self, sender):
        self.emit("show_now_playing_signal", True)


    def playbar_widget_slider_update(self, sender, progress):
        mins, seconds = divmod(progress, 60)
        formatted_progress = str(round(mins)) + ':' + str(round(seconds)).zfill(2)
        #print('Track Progress:', formatted_progress)
        self.playwidget_slider.set_range(0, self.player.player_get_track_duration())
        self.playwidget_slider.handler_block(self.playwidget_slider_handler_id)
        self.playwidget_slider.set_value(progress)
        self.play_widget_progress_duration.set_text(formatted_progress)
        self.playwidget_slider.handler_unblock(self.playwidget_slider_handler_id)

