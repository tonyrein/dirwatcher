"""
Strategy for updating playlists:

    In PlaylistUpdater:
    update_single_playlist() method is passed the name of the directory to update.
    If the directory does not exist or is empty:
        delete associated playlist file
    Else
        write the associated playlist file (deleting old contents, if any)

    In PlaylistMonitor:
    method clean_podast_playlists()
    for f in playlist_files:
        if corresponding directory does not exist or is empty:
            delete f

    PlaylistMonitor.run():
        calls clean_podcast_playlists()
        creates a dirwatcher.Watcher
        calls Watcher's loop() passing handle_watch_event()
        handle_watch_event:
            parses event and if it's a relevant one:
                find the directory it applies to
                call update_single_playlist() for that directory

"""
