import playlist_util

from pathlib import Path

def test_get_playlist_name_valid_top():
    p = Path('/media/user/VOLUME/Podcasts')
    assert playlist_util.get_playlist_name(p) == 'Podcasts.m3u'
    

def test_get_playlist_name_valid_sub():
    p = Path('/media/user/VOLUME/Podcasts/Walkabout')
    assert playlist_util.get_playlist_name(p) == 'Podcasts-Walkabout.m3u'
