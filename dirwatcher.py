from enum import IntFlag
from inotify.adapters import _INOTIFY_EVENT, InotifyTree

class EventFlag(IntFlag):
    """
    Values from inotify.constants wrapped
    in an IntFlag enum for convenience.
    """
    IN_CLOEXEC  = 0o2000000
    IN_NONBLOCK = 0o0004000

    ## Supported events suitable for MASK parameter of INOTIFY_ADD_WATCH.
    IN_ACCESS        = 0x00000001
    IN_MODIFY        = 0x00000002
    IN_ATTRIB        = 0x00000004
    IN_CLOSE_WRITE   = 0x00000008
    IN_CLOSE_NOWRITE = 0x00000010
    IN_OPEN          = 0x00000020
    IN_MOVED_FROM    = 0x00000040
    IN_MOVED_TO      = 0x00000080
    IN_CREATE        = 0x00000100
    IN_DELETE        = 0x00000200
    IN_DELETE_SELF   = 0x00000400
    IN_MOVE_SELF     = 0x00000800

    ## Helper events.
    IN_CLOSE         = (CLOSE_WRITE | CLOSE_NOWRITE)
    IN_MOVE          = (MOVED_FROM | MOVED_TO)

    ## All events which a program can wait on.
    IN_ALL_EVENTS    = (ACCESS | MODIFY | ATTRIB | CLOSE_WRITE |
                        CLOSE_NOWRITE | OPEN | MOVED_FROM | MOVED_TO | 
                        CREATE | DELETE | DELETE_SELF | MOVE_SELF)

    ## Events sent by kernel.
    IN_UNMOUNT    = 0x00002000 # Backing fs was unmounted.
    IN_Q_OVERFLOW = 0x00004000 # Event queued overflowed.
    IN_IGNORED    = 0x00008000 # File was ignored.

    ## Special flags.
    IN_ONLYDIR     = 0x01000000 # Only watch the path if it is a directory.
    IN_DONT_FOLLOW = 0x02000000 # Do not follow a sym link.
    IN_MASK_ADD    = 0x20000000 # Add to the mask of an already existing watch.
    IN_ISDIR       = 0x40000000 # Event occurred against dir.
    IN_ONESHOT     = 0x80000000 # Only send event once.


class EventInfo:
    def __init__(self, ev:tuple):
        in_ev_tuple:_INOTIFY_EVENT = ev[0]
        self.watch_descriptor = in_ev_tuple.wd
        self.mask = in_ev_tuple.mask
        self.cookie = in_ev_tuple.cookie
        self._length = in_ev_tuple.len
        self.event_names = ev[1]
        self.directory = ev[2]
        if len(ev) > 3:
            self.filename = ev[3]
        else:
            self.filename = 'NO FILE'

    def __len__(self) -> int:
        return self._length

    def __str__(self) -> str:
        return f"{self.event_names}: {self.directory} -> {self.filename}"

class Watcher:
    '''
    A wrapper around INotify functionality.
    Set it up by giving it
        * directory to monitor
        * set of events to monitor for
    Then call its loop() method, passing a callback
    function. The callback function will be called
    for each monitored event, and an EventInfo instance
    will be passed to it.
    '''
    def __init__(self,
        watch_dir:str='',
        flags:EventFlag=EventFlag.IN_ALL_EVENTS
    ):
        self.watch_dir = watch_dir
        self.event_flags = flags

    def loop(self, callback:callable):
        inot = InotifyTree(self.watch_dir, mask=self.event_flags)
        for ev in inot.event_gen(yield_nones=False):
            ev_info = EventInfo(ev)
            callback(ev_info)


        