"""
python run_audio.py channel_id
"""

import sys
from subprocess import Popen
from tempfile import TemporaryFile
from threading import Event, Thread

from yt import YTLiveService

processes = list()


def fprint(*args, **kwargs) -> None:
    print(*args, **kwargs, file=sys.stderr, flush=True)


def stop_audio():
    for p in processes:
        p.terminate()
    processes[:] = []


def play(link: str):
    fprint("Playing", link)
    stop_audio()
    p = Popen(
        ["mpv", "--no-video", link], stdout=TemporaryFile(), stderr=TemporaryFile()
    )


def main() -> None:
    fprint("Starting audio monitor of", sys.argv[1])
    ytl = YTLiveService(sys.argv[1])
    change = ytl.listen()
    while 1:
        if ytl.live_link:
            play(ytl.live_link)
        else:
            fprint("Vtuber not live", ytl.live_link)
        change.wait()
        change.clear()


if __name__ == "__main__":
    try:
        fprint("RUN AUDIO INVOKING MAIN")
        main()
    except (Exception, SystemExit):
        fprint("Exiting")
        stop_audio()
