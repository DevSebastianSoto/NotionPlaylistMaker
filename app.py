from decouple import config
from controllers import Spotify, Printable, Track, DataSongs, DataGenres


def write(fname: str, data: Printable):
    with open(file=f'{fname}.json', mode='w') as infile:
        infile.write(data.toJSON())


def init_spotify():
    scope = "user-read-email user-read-private \
    playlist-modify-public playlist-read-private playlist-modify-private"

    return Spotify(
        username=config("SPUSR"),
        scope=scope,
        client_id=config("CLIENT_ID"),
        client_secret=config("CLIENT_SECRET"),
        redirect_uri=config("REDIRECT_URI")
    )


def create_playlist(sp: Spotify, name: str, tracks: list) -> str:
    new_id = ""
    playlist_id = sp.playlist_exists(name)
    if playlist_id is None:
        sp.create_playlist(name)
        new_id = sp.playlist_exists(name)
    else:
        new_id = playlist_id
    sp.add_track_to_playlist(playlist_id=new_id, tracks=tracks)
    return new_id


if __name__ == "__main__":
    songs = DataSongs('songs.csv')
    sp = init_spotify()
    track_list = []
    df = songs.with_saxophone()
    for index, row in df.iterrows():
        name = row['Name']
        artist = row['Artists'][0]
        try:
            sptf_song = sp.search_track(
                name=name, artist=artist)
            song = Track(sptf_song)
            print(song.id)
            track_list.append(song.id)
        except Exception as exp:
            lmt = '---------------------------------'
            print(f'{lmt}\n{name} by {artist} NOT FOUND\n{lmt}')

    create_playlist(sp, 'Saxophone', track_list)
