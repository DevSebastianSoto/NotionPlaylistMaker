from decouple import config
from controllers import Spotify, Printable, Track


def write(fname: str, data: Printable):
    with open(file=f'{fname}.json', mode='w') as infile:
        infile.write(data.toJSON())


if __name__ == "__main__":
    SCOPE = "user-read-email user-read-private \
    playlist-modify-public playlist-read-private playlist-modify-private"

    sp = Spotify(
        username=config("SPUSR"),
        scope=SCOPE,
        client_id=config("CLIENT_ID"),
        client_secret=config("CLIENT_SECRET"),
        redirect_uri=config("REDIRECT_URI")
    )

    print(sp.playlist_exists('TEST'))
