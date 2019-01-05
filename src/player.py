#import os
#import urllib.request
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
    __gsignals__ =  {'player_state_change_signal' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (int,))}


    def __init__(self, gmusic):
        GObject.GObject.__init__(self)

        self.state = Player_State.STOPPED
        self.duration = 0
        self.current_playlist_position = -1
        self.playlist = []

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
        GObject.timeout_add(1000, self.player_update_slider)

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

    def player_add_to_playlist(self, playlist):
        for track in playlist:
            self.playlist.append(track)

    def player_get_playlist(self):
        return self.playlist
    
    def player_get_playing_track(self):
        return self.playlist[self.current_playlist_position]

    def player_on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)

    def player_get_state(self):
        return self.state


    '''
    def on_slider_seek(self, widget):
        seek_time_secs = self.slider.get_value()
        self.player.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, seek_time_secs * Gst.SECOND)

    '''

    def player_update_slider(self):
        #https://github.com/hadware/gstreamer-python-player/blob/master/seek.py
        if not self.state == Player_State.PLAYING:
            return False # cancel timeout
        else:
            success, self.duration = self.player.query_duration(Gst.Format.TIME)
            success, position = self.player.query_position(Gst.Format.TIME)
            print('Duration:', self.duration / Gst.SECOND, 'Position:', position / Gst.SECOND, 'Complete:', position / self.duration )
            return True

    def player_load_track(self, playlist_position):
        #playlist_index = playlist_position - 1
        track = self.playlist[playlist_position]
        track_id = track.get('id')
        #print('Play this track:', track_id)
        #TODO check stream url is valid
        track_url = self.gmusic.get_stream_url(track_id)
        self.player.set_property('uri', track_url)
        self.player_play()

    def player_get_next_track(self):
        self.player_stop()
        if len(self.playlist) > 0:
            if self.current_playlist_position < len(self.playlist):
                self.current_playlist_position = self.current_playlist_position + 1
                self.player_load_track(self.current_playlist_position)


    #def get_previous_track(self):




    
