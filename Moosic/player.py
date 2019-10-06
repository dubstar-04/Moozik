import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk
from .gmusicapi import *
from enum import Enum

class Player_State(Enum):
    STOPPED = 1
    PLAYING = 2
    PAUSED = 3

class Player(GObject.GObject):

    Gst.init(None)
    __gsignals__ =  {'player_state_change_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (int,)),
                     'player_progress_change_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (float,)),
                     'player_playlist_updated_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,))}


    def __init__(self, gmusic):
        GObject.GObject.__init__(self)

        self.state = Player_State.STOPPED
        self.duration = 0
        self.progress = 0
        self.current_playlist_position = -1
        self.playlist = []
        self.timeout_id = None

        self.gmusic = gmusic

        #GStreamer Player
        self.player = Gst.ElementFactory.make("playbin", "player")
        fakesink = Gst.ElementFactory.make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.player_on_message)

    def player_play(self):
        self.state = Player_State.PLAYING
        self.emit("player_state_change_signal", self.state.value)
        self.player.set_state(Gst.State.PLAYING)
        #self.timeout_id =
        #TODO how is this timer stopped?
        GObject.timeout_add(1000, self.player_update_progress)

    def player_pause(self):
        self.state = Player_State.PAUSED
        self.emit("player_state_change_signal", self.state.value)
        self.player.set_state(Gst.State.PAUSED)

    def player_stop(self):
        self.state = Player_State.STOPPED
        self.emit("player_state_change_signal", self.state.value)
        self.player.set_state(Gst.State.NULL)

    def player_clear_playlist(self):
        self.playlist = []
        self.current_playlist_position = -1

    def player_add_to_playlist(self, widget, tracks):
        for track in tracks:
        #track = self.gmusic.get_track_from_id(track_id)
            self.playlist.append(track)

        Utils().debug('playlist updated:', self.playlist)

    def player_remove_from_playlist(self, widget, index):
        self.playlist.pop(index)
        self.emit("player_playlist_updated_signal", True)


    def player_reorder_playlist(self, sender, indices):
        source_row = indices[0]
        destination_row = indices[1]
        Utils().debug('Player_reorder_playlist - move row:', source_row  ,'to row:', destination_row)

        if source_row < destination_row:
            self.playlist.insert(destination_row + 1, self.playlist[source_row])
            self.playlist.pop(source_row)
        else:
            self.playlist.insert(destination_row, self.playlist[source_row])
            self.playlist.pop(source_row + 1)

        self.emit("player_playlist_updated_signal", True)

    def player_get_playlist(self):
        return self.playlist
    
    def player_get_playing_track(self):
        return self.playlist[self.current_playlist_position]

    def player_on_message(self, bus, message):
        t = message.type
        #Utils().debug('dbus message:', t)
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            Utils().debug("Error: %s" % err, debug)

    def player_get_state(self):
        return self.state


    def player_seek(self, seek_position):
        Utils().debug('player_seek:', seek_position, 'duration:', self.duration)
        self.player.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, seek_position * Gst.SECOND)

    def player_update_progress(self):
        #https://github.com/hadware/gstreamer-python-player/blob/master/seek.py
        success, state, pending = self.player.get_state(Gst.CLOCK_TIME_NONE)
        #Utils().debug('player state:', state)
        if state == Gst.State.NULL:
            Utils().debug('Timer Stopped')
            self.player_get_next_track()
            return False
        else:
            success, track_duration = self.player.query_duration(Gst.Format.TIME)
            self.duration = track_duration / Gst.SECOND
            success, position = self.player.query_position(Gst.Format.TIME)
            self.progress = position / Gst.SECOND
            #Utils().debug('Player_progress:', self.progress, self.duration)
            self.emit("player_progress_change_signal", self.progress)
            return True

    def player_load_track(self, playlist_position):
        #playlist_index = playlist_position - 1
        track = self.playlist[playlist_position]
        track_id = track.get('moozik_id')
        Utils().debug('Play this track:', track_id)
        #TODO check stream url is valid
        track_url = self.gmusic.get_stream_url(track_id)
        self.player.set_property('uri', track_url)
        self.player_play()

    def player_get_next_track(self):
        self.player_stop()
        #TODO: indexing isnt correct
        if len(self.playlist) > 0:
            if self.current_playlist_position < len(self.playlist):
                self.current_playlist_position = self.current_playlist_position + 1
                self.player_load_track(self.current_playlist_position)

    def player_play_single_track(self, sender, track):
        #track = self.gmusic.get_track_from_id(track_id)
        Utils().debug('play:', track)
        self.player_clear_playlist()
        self.player_add_to_playlist(None, [track])
        self.player_get_next_track()

    def player_play_queue_track(self, sender, track):
        Utils().debug('play queue index:', track.get('title'))
        self.player_stop()
        for tr in range(len(self.playlist)):
            if self.playlist[tr] == track:
                self.current_playlist_position = tr
                self.player_load_track(tr)
                break


    def player_play_radio_station(self, sender, track_id):
        station_tracks = self.gmusic.get_radio_from_track(track_id)
        self.player_clear_playlist()

        track_ids = []
        for track in station_tracks:
            Utils().debug('player_radio_station_track:', track.get('storeId'))
            track_ids.append(track.get('storeId'))

        self.player_add_to_playlist(None, track_ids)
        self.player_get_next_track()

    def player_get_track_duration(self):
        return self.duration

    def player_get_track_progress(self):
        return self.progress



    
