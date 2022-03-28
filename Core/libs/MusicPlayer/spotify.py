import spotipy
from spotipy import SpotifyClientCredentials

from Core.enums.spotify_enums import SpotifyType, spotify_type
from Core.utils.dot_env import DotEnv


class SpotifyManager:

    def __init__(self):
        client_id = DotEnv.get('SPOTIFY_CLIENT')
        client_secret = DotEnv.get('SPOTIFY_SECRET')
        # self.client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,redirect_uri='http://example.com'))
        self.client = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    def get_playlist(self, spotify_id):
        playlist_item = self.client.playlist_items(spotify_id)
        return playlist_item

    def get_track(self, spotify_id):
        track = self.client.track(spotify_id)
        return track

    def get_album(self, spotify_id):
        album = self.client.album(spotify_id)
        return album

    def search(self, queue: str, type: SpotifyType):
        return self.client.search(queue, type=spotify_type(type))
