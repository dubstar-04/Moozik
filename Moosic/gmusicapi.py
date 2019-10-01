import gi
from gi.repository import GObject
import shutil, os, urllib.request
import gmusicapi #import Mobileclient

from oauth2client.client import OAuth2WebServerFlow
import oauth2client.file
import time

from .widgets import LoginDialog
from .utils import *
from .settings import *

from threading import Thread


class GmusicAPI(GObject.GObject):


    __gsignals__ =  {'api_logged_in' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (bool,)),
                     'api_albums_loaded' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (bool,GObject.TYPE_PYOBJECT)),
                     'api_playlists_loaded' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (bool,GObject.TYPE_PYOBJECT)),
                     'album_art_updated' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (bool,)),
                     'waiting_for_network' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (bool,))}


    def __init__(self):
        GObject.GObject.__init__(self)
        self.settings = Settings()
        self.api = gmusicapi.Mobileclient()
        self.library = None
        self.playlist_data = None
        self.search_results = []
        self.station_tracks = None
        self.albums = []
        self.playlists = []
        self.device_id = None
        self.logged_in = False

        try:
            #delete the temp art_cache
            shutil.rmtree(self.art_cache(temp=True))
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))

    def logout(self):

        print('gmusic logout')

        try:
            #delete the temp art_cache
            shutil.rmtree(self.art_cache(temp=True))
            shutil.rmtree(self.art_cache(temp=False))

            if os.path.isfile(self.oauth_filename()):
                os.remove(self.oauth_filename())

        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))


    def get_oauth_credentials(self):

        if os.path.isfile(self.oauth_filename()):
            return True
        else:
            flow = OAuth2WebServerFlow(**gmusicapi.session.Mobileclient().oauth._asdict())
            auth_uri = flow.step1_get_authorize_url()
            print('Auth URI', auth_uri)
            login_dialog = LoginDialog(auth_uri)
            login_dialog.run()
            code = login_dialog.get_code()
            credentials = flow.step2_exchange(code)
            storage = oauth2client.file.Storage(self.oauth_filename())
            storage.put(credentials)
            if os.path.isfile(self.oauth_filename()):
                return True
            else:
                return False

    def log_in(self):

        attempts = 0
        while not self.logged_in and attempts < 5:
            try:
               self.logged_in = self.api.oauth_login(device_id=gmusicapi.Mobileclient.FROM_MAC_ADDRESS, oauth_credentials=self.oauth_filename())
            except Exception as e:
                print('login failed', e)
            attempts += 1

        if not self.api.is_authenticated():
            self.emit('api_logged_in', False)
            return False
        else:
            self.emit('api_logged_in', True)
            self.device_id = self.get_device_id()
            return True

    def get_device_id(self):
        device_id = self.settings.get_device_id()
        if len(device_id):
            return device_id

        device_ids = self.api.get_registered_devices()
        device_id = device_ids[0].get("id").replace('0x', '')
        #TODO handle device_id being empty
        #device_id = gmusicapi.Mobileclient.FROM_MAC_ADDRESS
        if len(device_id):
            return device_id
        else:
            print ('failed to establish device id')

    def load_library(self):

        #check if there is an available network
        network = network_available()
        delay_login = not network

        while not network:
            #TODO stop waiting after x tries - show a reload button on the ui
            time.sleep(2)
            network = network_available()
            self.emit('waiting_for_network', True)

        if delay_login:
            time.sleep(5)
            self.emit('waiting_for_network', False)

        if self.get_oauth_credentials():
            print('Got oauth credentials')
            if self.log_in():
                print('logged_in')
                self.library = self.api.get_all_songs()
                self.load_albums()
                print('API Albums Loaded')
                self.playlist_data = self.api.get_all_user_playlist_contents()
                self.load_playlists()


                if len(self.albums):
                    print('Album count :', len(self.albums))
                    self.emit('api_albums_loaded', True, self.albums)
                    self.load_album_art(self.albums)
                if len(self.playlists):
                    print('Playlist count :', len(self.playlists))
                    self.emit('api_playlists_loaded', True, self.playlists)
                    self.load_album_art(self.playlists)
        else:
            print('Failed to get oauth credentials')
        #print(self.library)

    def load_albums(self):
        missing_art_count = 0
        for song in self.library:
            album_title = song.get("album")
            album_id = song.get("albumId")
            artist = song.get("artist")
            album_art_path = self.get_album_art_name(album_title)

            #add new key to song for a harmonized id
            song['moozik_id'] = song.get('id')
            song['album_art_path'] = album_art_path

            #TODO Should we always used the first album art?
            album_art_url = ''
            try:
                album_art_url = song.get("albumArtRef")[0].get("url")
            except Exception as e:
                missing_art_count += 1

            album = {'kind': 'album', 'title':album_title, 'album_id':album_id, 'artist':artist, 'album_art_url':album_art_url, 'album_art_path': album_art_path}

            #if album not in self.albums:
            if not any(album.get('title', None) == album_title for album in self.albums):
                self.albums.append(album)

        print('Missing Album Art:', missing_art_count)

    def load_playlists(self):
        missing_art_count = 0
        #playlists = self.api.get_all_playlists()
        #playlists = self.api.get_all_user_playlist_contents()

        for playlist in self.playlist_data:
            #print('\nPlaylist:', playlist.get('name'))
            #print(playlist)
            album_title = playlist.get("name")
            album_id = playlist.get("playlistId")
            artist = playlist.get("ownerName")
            album_art_path = self.get_album_art_name(album_title)



            for playlist_track in playlist.get('tracks'):
                track_id = playlist_track.get('trackId')

                #if playlist_track.get('source') == '1':
                if 'track' not in playlist_track:
                    playlist_track['track'] = {}
                    for song in self.library:
                        if song.get('id') == track_id:
                            playlist_track['track'] = song

                track = playlist_track.get('track')

                album_art_url = ''
                try:
                    album_art_url = track.get("albumArtRef")[0].get("url")
                except Exception as e:
                    missing_art_count += 1

                try:
                    playlist['album_art_path'] = album_art_path

                    track['moozik_id'] = track_id
                    track['album_art_path'] = album_art_path
                    track['album_art_url'] = album_art_url

                    #TODO: Look up track data from id
                    if 'title' not in track:
                        track['title'] = 'title error'
                    if 'artist' not in track:
                        track['artist'] = 'artist error'
                    if 'albumArtist' not in track:
                        track['albumArtist'] = 'album artist error'
                    if 'album' not in track:
                        track['album'] = 'album error'

                except:
                    print('load_playlists: track error')

            #add playlist to self.playlists
            pl = {'kind': 'playlist', 'title':album_title, 'album_id':album_id, 'artist':artist, 'album_art_url':album_art_url, 'album_art_path': album_art_path}
            self.playlists.append(pl)


        print('Missing Playlist Art:', missing_art_count)


    def search_library(self, search_query):

        self.search_results = []

        if len(search_query):
            search_hits = self.api.search(search_query, max_results=10)
            if search_hits:
                for source, data in search_hits.items():
                     if  source == 'album_hits' or source == 'song_hits':
                        for entry in data:
                            for key, value in entry.items():
                                if key == 'album' or key == 'track':
                                    print('data:', value)

                                    item = value

                                    _title = 'name'
                                    _album = 'name'
                                    store_id = ''


                                    if key == 'track':
                                        _title = 'title'
                                        _album = 'album'
                                        store_id = item.get("storeId")

                                    album_title = item.get(_title)
                                    album = item.get(_album)
                                    album_art_path = self.get_album_art_name(album_title, True)
                                    album_id = item.get("albumId")
                                    artist = item.get("artist")


                                    album_art_url = ''
                                    try:
                                        if key == 'album':
                                            album_art_url = item.get("albumArtRef")
                                        else:
                                            album_art_url = item.get("albumArtRef")[0].get("url")
                                    except Exception:
                                        #print('no album art available')
                                        pass

                                    item_data = {'kind': item.get('kind'), 'title':album_title, 'album':album, 'album_id':album_id, 'storeId':store_id, 'moozik_id':store_id, 'artist':artist, 'album_art_url':album_art_url, 'album_art_path': album_art_path}
                                    self.search_results.append(item_data)

                self.load_album_art(self.search_results)


            #hit: artist_hits
            #hit: playlist_hits
            #hit: genre_hits
            #hit: podcast_hits
            #hit: situation_hits
            #hit: song_hits
            #hit: station_hits
            #hit: video_hits

    #TODO Impliment some type of lazy loading for the album art
    def load_album_art(self, albums):

        init_thread = Thread(target=self.download_album_art, args=[albums])
        #init_thread.daemon = True
        init_thread.start()

    def download_album_art(self, albums):
        for album in albums:
            file_path = album.get('album_art_path')
            art_url = album.get('album_art_url')
            #print('art_url:', art_url, 'Path:', file_path)
            if len(art_url):
                if not os.path.isfile(file_path):
                    print('file path:', file_path, ' url: ', art_url)
                    try:
                        urllib.request.urlretrieve(art_url, file_path)

                    except Exception as e:
                        print('Artwork could not be downloaded:', e)
        GObject.idle_add(self.emit, 'album_art_updated', True)

    def get_library(self):
        return self.library

    def get_albums(self):
        return self.albums

    def get_search_results(self):
        return self.search_results

    def oauth_filename(self):
        xdg_cache_dir = os.environ.get('XDG_CACHE_HOME')
        cache_dir = os.path.join(xdg_cache_dir, 'oauth')
        try:
            os.makedirs(cache_dir, mode=0o755, exist_ok=True)
        except EnvironmentError:
            return None
        else:
            oauth_filename = os.path.join(cache_dir, 'oauth.cred')
            return oauth_filename

    def art_cache(self, temp):
        dir_name = 'album_art'
        if temp:
            dir_name = 'temp_album_art'

        xdg_cache_dir = os.environ.get('XDG_CACHE_HOME')
        cache_dir = os.path.join(xdg_cache_dir, dir_name)
        try:
            os.makedirs(cache_dir, mode=0o755, exist_ok=True)
        except EnvironmentError:
            return None
        else:
            return cache_dir

    def get_album_art_name(self, album_title, temp=False):
        album_title = slugify(album_title)
        return self.art_cache(temp) + '/' + album_title + '.jpg'

    def get_album(self, album_index):
        return self.albums[album_index]

    def get_album_tracks(self, album_index, kind):

        tracks = []

        if kind == 'album':
            album_title = self.albums[album_index].get('title')
            for song in self.library:
                if song.get('album') == album_title:
                    tracks.append(song)

        if kind == 'playlist':
            album_title = self.playlist_data[album_index].get('name')

            print('Playlist Selected:', album_title)
            playlist_tracks = self.playlist_data[album_index].get('tracks')

            #print('playlist:', playlist_tracks)

            for track in playlist_tracks:
                try:
                    #print(track.get('track').get('title'))
                    tracks.append(track.get('track'))
                except:
                    print('Track Error')


            #for song in self.playlist_data[album_index]:
                #print (song.get('playlistId'), album_title)
                #if song.get('playlistId') == album_title:
                #    tracks.append(song)

        return tracks

    def get_album_info(self, albumId):
        ''' get album data and tracks for seached items'''
        album_info = self.api.get_album_info(albumId, include_tracks=True)

        tracks = []
        for track in album_info.get('tracks'):

            album_title = track.get("album")
            album_art_path = self.get_album_art_name(album_title, True)

            track['moozik_id'] = track.get('storeId')
            track['album_art_path'] = album_art_path

            tracks.append(track)

        return tracks

    def get_stream_url(self, track_id):
        #TODO handle url errors
        #TODO check the track_id exists?
        #TODO check the device_id isnt null
        track_url = self.api.get_stream_url(track_id, self.device_id)
        print('Stream Url',track_url)
        return track_url

    def get_album_from_id(self, albumId):
        for album in self.albums:
            if album.get('albumId') == albumId:
                return album

    def get_track_from_id(self, track_id):
        for track in self.library:
            if track.get('storeId') == track_id:
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


