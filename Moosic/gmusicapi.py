import gi
from gi.repository import GObject
import os, urllib.request, string
from gmusicapi import Mobileclient
from .settings import *

class GmusicAPI(GObject.GObject):


    __gsignals__ =  {'api_logged_in' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (bool,)),
                     'api_albums_loaded' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (bool,))}


    def __init__(self):
        GObject.GObject.__init__(self)
        self.settings = Settings()
        self.api = Mobileclient()
        self.library = None
        self.station_tracks = None
        self.albums = []
        self.playlists = None
        self.device_id = None
        self.logged_in = False


    def api_init(self):
        print('Starting API init thread')
        if self.log_in():
            self.device_id = self.get_device_id()

        self.load_library()

    #TODO Use OAuth
    def log_in(self):

        username = self.settings.get_username()
        password = self.settings.get_password()
        
        attempts = 0

        while not self.logged_in and attempts < 3:
            try:
                logged_in = self.api.login(username, password, Mobileclient.FROM_MAC_ADDRESS)
            except Exception:
                print('login failed')

            attempts += 1

        if not self.api.is_authenticated():
            self.emit('api_logged_in', False)
            return False
        else:
            self.emit('api_logged_in', True)
            return True

    def get_device_id(self):

        device_id = self.settings.get_device_id()
        if len(device_id):
            return device_id

        device_ids = self.api.get_registered_devices()
        device_id = device_ids[0].get("id").replace('0x', '')
        if len(device_id):
            return device_id
        else:
            print ('failed to establish device id')

    def load_library(self):
        self.library = self.api.get_all_songs()
        self.load_albums()
        print('API Albums Loaded')

        if len(self.albums):
            print('Album count :', len(self.albums))
            self.emit('api_albums_loaded', True)

        self.load_album_art()

        #print(self.library)

    #TODO Move this out of the UI thread
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


    #TODO Impliment some type of lazy loading for the album art
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

    #TODO Move to a helper module
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
        #TODO handle url errors
        #TODO check the track_id exists?
        #TODO check the device_id isnt null
        track_url = self.api.get_stream_url(track_id, self.device_id)
        print('Stream Url',track_url)
        return track_url

    def get_track_from_id(self, track_id):
        for track in self.library:
            if track.get('id') == track_id:
                #print('Match:', track_id, track.get('storeId'))
                return track
        #TODO Handle the stations tracks better. id vs storeId should be transparent
        if self.station_tracks:
            for track in self.station_tracks:
                if track.get('storeId') == track_id:
                    return track

    def get_radio_from_track(self, track_id):
        station_name = 'moosic'
        station_id = self.api.create_station(station_name, track_id, artist_id=None, album_id=None, genre_id=None, playlist_token=None, curated_station_id=None)
        print('station_id:', station_id)
        station_tracks = self.get_station_tracks(station_id)
        return station_tracks

    def get_station_tracks(self, station_id):
        #TODO impliment station_id 'IFL' for the “I’m Feeling Lucky” station.
        #station_id = 'IFL'
        self.station_tracks = self.api.get_station_tracks(station_id, num_tracks=20, recently_played_ids=None)
        print('radio station tracks:', len(self.station_tracks))
        return self.station_tracks


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


