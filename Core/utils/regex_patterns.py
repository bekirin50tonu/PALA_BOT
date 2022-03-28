import re

from Core.enums.spotify_enums import Platform, SpotifyType

youtube_regex = (
    r'(https?://)?(www\.)?'
    '(youtube|youtu|youtube-nocookie)\.(com|be)/'
    '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

spotify_regex = r"^(?:spotify:|https:\/\/[a-z]+\.spotify\.com\/|(playlist\/|user\/(.*)\/playlist\/))(.*)$"

spotify_playlist_pattern = r'https:(.*?)\/playlist\/(.*?)\?(.*)'

spotify_track_pattern = r'https:(.*?)\/track\/(.*?)\?(.*)'

spotify_album_pattern = r'https:(.*?)\/album\/(.*?)\?(.*)'


def url_validation(url):
    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return url, Platform.YOUTUBE
    spotify_regex_match = re.search(spotify_regex, url)
    if spotify_regex_match:
        return url, Platform.SPOTIFY
    print(youtube_regex_match, spotify_regex_match)
    return url, Platform.NOTHING


def split_spotify_variables(url):
    try:
        data = re.search(spotify_album_pattern, url)
        if data:
            return data, SpotifyType.Album
        data = re.search(spotify_track_pattern, url)
        if data:
            return data, SpotifyType.Track
        data = re.search(spotify_playlist_pattern, url)
        if data:
            return data, SpotifyType.Playlist
        return data, SpotifyType.Notype
    except Exception as e:
        print('regex-'+str(e))
