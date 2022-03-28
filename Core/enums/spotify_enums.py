from enum import Enum


class Platform(Enum):
    YOUTUBE = 1
    SPOTIFY = 2
    NOTHING = 3


class SpotifyType(Enum):
    Playlist = 1
    Track = 2
    Album = 3
    Notype = 4


def spotify_type(spo_type: SpotifyType):
    if spo_type is SpotifyType.Track:
        return 'track'
    elif spo_type is SpotifyType.Playlist:
        return 'playlist'
    elif spo_type is SpotifyType.Album:
        return 'album'
    else:
        return 'none'
