from urllib3.util import parse_url
import json
import spotipy
from spotipy.util import prompt_for_user_token


class Spotify:
    def __init__(self, username, scope, client_id, client_secret, redirect_uri):
        self.__username = username
        token = prompt_for_user_token(
            username=username,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri
        )
        self.__instance = spotipy.Spotify(auth=token)

    @property
    def playlists(self):
        return self.__instance.user_playlists(self.__username)['items']

    def new_playlist(self, name, description)

    def search_track(self, name, artist):
        query = f'{name} artist:{artist}'
        return self.__instance.search(q=query, limit=1, type='track')

    def playlist_exists(self, name) -> bool:
        for playlist in self.playlists:
            if playlist['name'] == name:
                return True
        return False


class Printable():
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Track(Printable):
    def __init__(self, jdata: dict):
        track = jdata['tracks']['items'][0]
        self.__id = track['id']
        self.__name = track['name']
        self.__artist_id = track['artists'][0]['id']

