from pathlib import Path
from typing import List

# constants
PODCAST_TOPDIR = 'Podcasts'
PODCAST_EXT = 'mp3'
PLAYLIST_EXT = 'm3u'
PLAYLIST_DIR = 'Playlists'
PLAYLIST_HEADER = '#EXTM3U'
WIN_PATH_SEP = '\r\n'

def get_playlist_name(p:Path) -> str:
    """
    The path passed to this method will be either
    the top-level podcast directory, or a subdirectory
    one level below the top-level podcast directory.

    If top-level, return 'Podcast.m3u'
    If in subdirectory 'Sub', return 'Podcast-Sub.m3u'

    If neither last nor next-to-last element of path is 
    the top-level podcast directory name, raise a
    ValueError.

    """
    parts = p.absolute().parts
    last_part = parts[-1]
    if last_part == PODCAST_TOPDIR:
        return f"{PODCAST_TOPDIR}.{PLAYLIST_EXT}"
    else:
        if (len(parts) < 2) or (parts[-2] != PODCAST_TOPDIR):
            raise ValueError(f'{p} is not a valid podcast directory')
        return f"{PODCAST_TOPDIR}-{last_part}.{PLAYLIST_EXT}"


def get_directory_list(p:Path, descend:bool=False) -> List[Path]:
    ret_list = [ p ]
    if descend:
        ret_list += [ i for i in p.rglob('*') if i.is_dir() ]
    else:
        ret_list += [ i for i in p.iterdir() if i.is_dir() ]
    return ret_list

def get_file_list(p:Path, descend:bool=False, glob_mask:str='*') -> List[Path]:
    if descend:
        return [ f for f in p.rglob(glob_mask) ]
    else:
        return [ f for f in p.glob(glob_mask) ]