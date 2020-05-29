import json
import spotipy
from spotipy.util import prompt_for_user_token
from urllib3.util import parse_url
import pandas as pd
from abc import ABC, abstractmethod


class DataAccess(ABC):
    def __init__(self, file_path: str):
        self._df = pd.read_csv(file_path)
        self._df = self.clean_data()

    @abstractmethod
    def data(self):
        pass

    @abstractmethod
    def clean_data(self):
        pass

    @staticmethod
    def filter_url_field(field: str) -> list:
        urls = field.split(',')
        res = []
        for url in urls:
            res.append(' '.join(url.split('/')[-1].split('-')[:-1]))
        return res


class DataGenres(DataAccess):
    def __init__(self, file_path):
        super(DataGenres, self).__init__(file_path)

    @property
    def data(self):
        return self._df.astype({'Name': str, 'Genre': list})

    def clean_data(self):
        return self._df


class DataSongs(DataAccess):
    def __init__(self, file_path):
        super(DataSongs, self).__init__(file_path)

    @property
    def data(self):
        return self._df.drop(columns=['Music Sheet'])

    def clean_data(self) -> pd.DataFrame:
        df = self._df
        df['Artists'] = df['Artists'].apply(
            lambda row: self.filter_url_field(row))
        df['Genre'] = df['Genre'].apply(
            lambda row: self.filter_url_field(row))
        return df

    def __instrument_filter(self, instrument: str) -> pd.DataFrame:
        return self._df[self._df[instrument] == 'Yes']

    def with_saxophone(self) -> pd.DataFrame:
        return self.__instrument_filter('Saxophone').drop(columns=['Saxophone'])


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

    def create_playlist(self, name, description=""):
        self.__instance.user_playlist_create(
            self.__username, name=name, description=description)

    def search_track(self, name, artist):
        query = f'{name} artist:{artist}'
        return self.__instance.search(q=query, limit=1, type='track')

    def playlist_exists(self, name) -> str:
        for playlist in self.playlists:
            if playlist['name'] == name:
                return playlist['id']
        return None

    def add_track_to_playlist(self, playlist_id: str, tracks: list):
        self.__instance.user_playlist_add_tracks(
            self.__username, playlist_id=playlist_id, tracks=tracks)


class Printable():
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Track(Printable):
    def __init__(self, jdata: dict):
        track = jdata['tracks']['items'][0]
        self.__id = track['uri']
        self.__name = track['name']
        self.__artist_id = track['artists'][0]['id']

    @property
    def id(self):
        return self.__id
