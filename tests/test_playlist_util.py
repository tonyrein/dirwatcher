import playlist_util

import pytest

from pathlib import Path
import shutil


@pytest.fixture
def example_path() -> Path:
    example_name = '/tmp/Podcasts'
    p = Path(example_name)
    if p.exists():
        shutil.rmtree(p)
    subdirs = [ 'A/1', 'A/2', 'B/1', 'B/2', 'C/1', 'C/2' ]
    for s in subdirs:
        psub = p / s
        psub.mkdir(parents=True, exist_ok=True)
    dirlist = [p] + [ i for i in p.rglob('*') if i.is_dir() ]
    for d in dirlist:
        pmp3 = d / f"{d.name}.mp3"
        pmp3.touch()
    yield p
    shutil.rmtree(p)



def test_get_playlist_name_valid_top():
    p = Path('/media/user/VOLUME/Podcasts')
    assert playlist_util.get_playlist_name(p) == 'Podcasts.m3u'
    

def test_get_playlist_name_valid_sub():
    p = Path('/media/user/VOLUME/Podcasts/Walkabout')
    assert playlist_util.get_playlist_name(p) == 'Podcasts-Walkabout.m3u'

def test_get_playlist_name_invalid_top():
    p = Path('/media/user/VOLUME/nosuchdirectory')
    with pytest.raises(ValueError) as e_info:
        playlist_util.get_playlist_name(p)
    assert f'{p} is not a valid podcast directory' in str(e_info.value)

def test_get_playlist_name_invalid_sub():
    p = Path('/media/user/VOLUME/nosuchdirectory/Walkabout')
    with pytest.raises(ValueError) as e_info:
        playlist_util.get_playlist_name(p)
    assert f'{p} is not a valid podcast directory' in str(e_info.value)

def test_get_directory_list_flat(example_path):
    dirlist = playlist_util.get_directory_list(example_path, descend=False)
    dnames = [
        '/tmp/Podcasts',
        '/tmp/Podcasts/A',
        '/tmp/Podcasts/B',
        '/tmp/Podcasts/C'
        ]
    checklist = [ Path(s) for s in dnames ]
    assert (
        all( d in checklist for d in dirlist ) and 
        len(dirlist) == len(checklist)
    )
 
def test_get_directory_list_recursive(example_path):
    dirlist = playlist_util.get_directory_list(example_path, descend=True)
    dnames = [
        '/tmp/Podcasts',
        '/tmp/Podcasts/A',
        '/tmp/Podcasts/B',
        '/tmp/Podcasts/C',
        '/tmp/Podcasts/A/1',
        '/tmp/Podcasts/A/2',
        '/tmp/Podcasts/B/1',
        '/tmp/Podcasts/B/2',
        '/tmp/Podcasts/C/1',
        '/tmp/Podcasts/C/2'  
    ]
    checklist = [ Path(s) for s in dnames ]
    assert (
        all( d in checklist for d in dirlist ) and 
        len(dirlist) == len(checklist)
    )
