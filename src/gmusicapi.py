from gmusicapi import Mobileclient
from .settings import *



class GmusicAPI():
    def __init__(self):
        self.settings = Settings()
        self.api = Mobileclient()
        self.library = None
        self.playlists = None


    def logged_in(self):

        logged_in = False
        attempts = 0
        
        username = self.settings.get_username()
        password = self.settings.get_password()
        
        print(username, password)

        while not logged_in and attempts < 3:
            logged_in = self.api.login(username, password, Mobileclient.FROM_MAC_ADDRESS)
            attempts += 1

        #return logged_in
    
        if not self.api.is_authenticated():
            print("Sorry, those credentials weren't accepted.")
            return False
        else:
            print("Success, credentials accepted.")
            self.load_library()
            #self.load_playlists()
            return True
        

    def load_library(self):
        self.library = self.api.get_all_songs()
        #print(self.library)
        
    def load_playlists(self):
        self.playlists = self.api.get_all_playlists()
        #print(self.playlists)

    def get_library(self):
        return self.library

'''
    def get_all_songs(self):
    def get_stream_url(self):
    def rate_songs(self):
    def change_song_metadata(self):
    def delete_songs(self):
    def get_promoted_songs(self):
    def increment_song_playcount(self):
    def add_store_track(self):
    def add_store_tracks(self):
    def get_station_track_stream_url(self):
'''       



#playlists
'''
    def get_all_playlists(self):
    def get_all_user_playlist_contents(self):
    def get_shared_playlist_contents(self):
    def create_playlist(self):
    def delete_playlist(self):
    def edit_playlist(self):
    def add_songs_to_playlist(self):
    def remove_entries_from_playlist(self):
    def reorder_playlist_entry(self):
'''
