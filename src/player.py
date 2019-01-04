#import os
#import urllib.request
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk

from enum import Enum

class Player_State(Enum):
    STOPPED = 1
    PLAYING = 2
    PAUSED = 3

class Player():

    Gst.init(None)

    def __init__(self):
        self.state = None
        self.playlist = []

        self.player = Gst.ElementFactory.make("playbin", "player")
        fakesink = Gst.ElementFactory.make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def player_play(self, track_url):
        print('Player Play:', track_url)
        self.state = Player_State.PLAYING
        self.player.set_property('uri', track_url)
        #self.player.set_state(Gst.STATE_PLAYING)
        self.player.set_state(Gst.State.PLAYING)

    def player_pause():
        self.state = Player_State.PAUSED

    def player_stop():
        self.state = Player_State.STOPPED
        self.player.set_state(Gst.State.NULL)

    def add_to_playlist(self, playlist):
        for track in playlist:
            self.playlist.append(track)

    def get_playlist(self):
        return self.playlist
    
    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)

    
