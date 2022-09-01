import playlist_util

import pytest

from pathlib import Path
import shutil


@pytest.fixture
def sample_path() -> Path:
    '''
    Make a temporary folder structure to use for testing
    '''
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
    # make an empty subdirectory:
    pempty = p / 'D/1'
    pempty.mkdir(parents=True, exist_ok=True)
    yield p
    shutil.rmtree(p)

def test_lists_have_same_members():
    list1 = [ 'a', 'b', 'c', 'd' ]
    list2 = [ 'b', 'c', 'd', 'a' ]
    assert playlist_util.lists_have_same_members(list1, list2)

def test_lists_have_different_members():
    list1 = [ 'a', 'b', 'c', 'd' ]
    list2 = [ 'b', 'c', 'd', 'e' ]
    assert not playlist_util.lists_have_same_members(list1, list2)


def test_lists_have_different_member_count():
    list1 = [ 'a', 'b', 'c', 'd' ]
    list2 = [ 'b', 'c', 'd', 'a', 'a' ]
    assert not playlist_util.lists_have_same_members(list1, list2)

def test_get_playlist_name_valid_top():
    p = Path('/media/user/VOLUME/Podcasts')
    assert playlist_util.get_playlist_name(p) == p / 'Podcasts.m3u'    

def test_get_playlist_name_valid_sub_first_level():
    p = Path('/media/user/VOLUME/Podcasts/Walkabout')
    assert playlist_util.get_playlist_name(p) == p / 'Podcasts-Walkabout.m3u'

def test_get_playlist_name_valid_sub_second_level():
    p = Path('/media/user/VOLUME/Podcasts/Walkabout/03')
    assert playlist_util.get_playlist_name(p) == p.parent / 'Podcasts-Walkabout.m3u'

def test_get_playlist_name_invalid_top():
    p = Path('/media/user/VOLUME/nosuchdirectory')
    with pytest.raises(ValueError) as e_info:
        playlist_util.get_playlist_name(p)
    assert f"{p} is not a valid podcasts directory name" in str(e_info.value)

def test_get_playlist_name_invalid_sub():
    p = Path('/media/user/VOLUME/nosuchdirectory/Walkabout')
    with pytest.raises(ValueError) as e_info:
        playlist_util.get_playlist_name(p)
    assert f"{p} is not a valid podcasts directory name" in str(e_info.value)

def test_get_directory_list_flat(sample_path):
    dirlist = playlist_util.get_directory_list(sample_path, descend=False)
    dnames = [
        '/tmp/Podcasts',
        '/tmp/Podcasts/A',
        '/tmp/Podcasts/B',
        '/tmp/Podcasts/C',
        '/tmp/Podcasts/D',
        ]
    checklist = [ Path(s) for s in dnames ]
    assert playlist_util.lists_have_same_members(checklist, dirlist)
 
def test_get_directory_list_recursive(sample_path):
    dirlist = playlist_util.get_directory_list(sample_path, descend=True)
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
        '/tmp/Podcasts/C/2',
        '/tmp/Podcasts/D',
        '/tmp/Podcasts/D/1'
    ]
    checklist = [ Path(s) for s in dnames ]
    assert playlist_util.lists_have_same_members(checklist, dirlist)

def test_get_all_mp3_files(sample_path):
    mp3list = playlist_util.get_file_list(p=sample_path, descend=True, glob_mask='*.[mM][pP]3')
    fnames = [
        '/tmp/Podcasts/A/1/1.mp3',
        '/tmp/Podcasts/A/2/2.mp3',
        '/tmp/Podcasts/A/A.mp3',
        '/tmp/Podcasts/B/1/1.mp3',
        '/tmp/Podcasts/B/2/2.mp3',
        '/tmp/Podcasts/B/B.mp3',
        '/tmp/Podcasts/C/1/1.mp3',
        '/tmp/Podcasts/C/2/2.mp3',
        '/tmp/Podcasts/C/C.mp3',
        '/tmp/Podcasts/Podcasts.mp3',

    ]
    checklist = [ Path(s) for s in fnames ]
    assert playlist_util.lists_have_same_members(checklist, mp3list)

def test_get_mp3_files_for_subdir_with_files(sample_path):
    subpath = sample_path / 'B'
    mp3list = playlist_util.get_file_list(p=subpath, descend=True, glob_mask='*.[mM][pP]3')
    fnames = [
        '/tmp/Podcasts/B/1/1.mp3',
        '/tmp/Podcasts/B/2/2.mp3',
        '/tmp/Podcasts/B/B.mp3',
    ]
    checklist = [ Path(s) for s in fnames ]
    assert playlist_util.lists_have_same_members(checklist, mp3list)

def test_get_mp3_files_for_empty_subdir(sample_path):
    subpath = sample_path / 'D'
    mp3list = playlist_util.get_file_list(p=subpath, descend=True, glob_mask='*.[mM][pP]3')
    assert mp3list == []

def test_get_mp3_files_toplevel(sample_path):
    mp3list = playlist_util.get_file_list(p=sample_path, descend=False, glob_mask='*.[mM][pP]3')
    fnames = [
        '/tmp/Podcasts/Podcasts.mp3',
    ]
    checklist = [ Path(s) for s in fnames ]
    assert playlist_util.lists_have_same_members(checklist, mp3list)

def test_get_pod_directory_path_top():
    s = '/tmp/Podcasts'
    path_to_check = Path(s)
    right_answer_path = Path(s)
    assert playlist_util.get_pod_directory_path(path_to_check) == right_answer_path

def test_get_pod_directory_path_sub_one_level():
    s = '/tmp/Podcasts/03'
    path_to_check = Path(s)
    right_answer_path = Path(s)
    assert playlist_util.get_pod_directory_path(path_to_check) == right_answer_path

def test_get_pod_directory_path_sub_multiple_levels():
    topsub = '/tmp/Podcasts/03'
    lowersub = f'{topsub}/sub_d'
    path_to_check = Path(lowersub)
    right_answer_path = Path(topsub)
    assert playlist_util.get_pod_directory_path(path_to_check) == right_answer_path

def test_get_pod_directory_invalid_path():
    s = '/tmp/nosuchdirectory/27/lower'
    p = Path(s)
    with pytest.raises(ValueError) as e_info:
        playlist_util.get_pod_directory_path(p)
    assert f"{p} is not a valid podcasts directory name" in str(e_info.value)

def test_list_mp3_files_for_pod_directory_top(sample_path):
    fname = '/tmp/Podcasts/Podcasts.mp3'
    checklist = [ Path(fname) ]
    mp3list = playlist_util.list_mp3_files_for_pod_directory(sample_path)
    assert playlist_util.lists_have_same_members(checklist, mp3list)

def test_list_mp3_files_for_pod_directory_sub_first_level(sample_path):
    path_to_read = sample_path / 'C'
    fnames = [
        '/tmp/Podcasts/C/1/1.mp3',
        '/tmp/Podcasts/C/2/2.mp3',
        '/tmp/Podcasts/C/C.mp3',
    ]
    checklist = [ Path(s) for s in fnames ]
    mp3list = playlist_util.list_mp3_files_for_pod_directory(path_to_read)
    assert playlist_util.lists_have_same_members(checklist, mp3list)

def test_list_mp3_files_for_pod_directory_sub_second_level(sample_path):
    path_to_read = sample_path / 'C/2'
    fnames = [
        '/tmp/Podcasts/C/1/1.mp3',
        '/tmp/Podcasts/C/2/2.mp3',
        '/tmp/Podcasts/C/C.mp3',
    ]
    checklist = [ Path(s) for s in fnames ]
    mp3list = playlist_util.list_mp3_files_for_pod_directory(path_to_read)
    assert playlist_util.lists_have_same_members(checklist, mp3list)
