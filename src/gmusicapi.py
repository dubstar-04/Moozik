from gmusicapi import Mobileclient
from .settings import *

import os
import urllib.request
#import re
import string

class GmusicAPI():
    def __init__(self):
        self.settings = Settings()
        self.api = Mobileclient()
        self.library = None
        self.albums = []
        self.playlists = None
        self.device_id = None


    #TODO Use OAuth
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
            self.get_device_id()
            self.load_library()
            #self.load_playlists()
            return True

    def get_device_id(self):
        device_ids = self.api.get_registered_devices()
        #print('device_ids:', device_ids)
        self.device_id = device_ids[0].get("id").replace('0x', '')
        print('Device ID:', self.device_id)

    def load_library(self):
        self.library = self.api.get_all_songs()
        self.load_albums()
        self.load_album_art()
        print('Album count :', len(self.albums))
        #print(self.library)

    def load_albums(self):
        for song in self.library:
            album_title = song.get("album")
            album_id = song.get("albumId")
            artist = song.get("artist")
            album_art_path = self.get_album_art_name(album_title)

            #TODO Should we always used the first album art?
            album_art_url = ''
            try:
                album_art_url = song.get("albumArtRef")[0].get("url")
            except Exception:
                print('no album art available')

            album = {'title':album_title, 'album_id':album_id, 'artist':artist, 'album_art_url':album_art_url, 'album_art_path': album_art_path}

            #if album not in self.albums:
            if not any(album.get('title', None) == album_title for album in self.albums):
                self.albums.append(album)

    def load_album_art(self):
        for album in self.albums:
            file_path = album.get('album_art_path')
            art_url = album.get('album_art_url')
            if len(art_url):
                if not os.path.isfile(file_path):
                    print('file path:', file_path, ' url: ', art_url)
                    try:
                        urllib.request.urlretrieve(art_url, file_path)
                    except Exception:
                        print('Artwork could not be downloaded:', Exception)

    def load_playlists(self):
        self.playlists = self.api.get_all_playlists()
        #print(self.playlists)

    def get_library(self):
        return self.library

    def get_albums(self):
        return self.albums

    def art_cache(self):
        xdg_cache_dir = os.environ.get('XDG_CACHE_HOME')

        cache_dir = os.path.join(xdg_cache_dir, 'album_art')

        try:
            os.makedirs(cache_dir, mode=0o755, exist_ok=True)
        except EnvironmentError:
            return None
        else:
            return cache_dir

    def get_album_art_name(self, album_title):
        album_title = self.slugify(album_title)
        return self.art_cache() + '/' + album_title + '.jpg'

    #TODO Move to a support class
    def slugify(self, s):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in s if c in valid_chars)
        filename = filename.replace(' ','-')
        return filename

    def get_album(self, album_index):
        return self.albums[album_index]

    def get_album_tracks(self, album_index):

        album_title = self.albums[album_index].get('title')

        tracks = []

        for song in self.library:
            if song.get('album') == album_title:
                tracks.append(song)

        return tracks

    def get_stream_url(self, track_id):
        track_url = self.api.get_stream_url(track_id, self.device_id)
        print('Stream Url',track_url)
        return track_url

    def get_track_from_id(self, track_id):
        for track in self.library:
            if track.get('id') == track_id:
                return track


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
