import os
import urllib.request

from enum import Enum

class Player_State(Enum):
    STOPPED = 1
    PLAYING = 2
    PAUSED = 3

class Player():
    def __init__(self):
        self.state = None
        self.playlist = []

    def player_play(playlist):
        self.state = Player_State.PLAYING

    def player_pause():
        self.state = Player_State.PAUSED

    def player_stop():
        self.state = Player_State.STOPPED

    def add_to_playlist(self, playlist):
        for track in playlist:
            self.playlist.append(track)

    def get_playlist(self):
        return self.playlist
    
