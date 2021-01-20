"""
python run_audio.py channel_id
"""

import sys
from subprocess import Popen
from tempfile import TemporaryFile
from threading import Event, Thread

from yt import YTLiveService

processes = list()


def stop_audio():
    for p in processes:
        p.terminate()
    processes[:] = []


def play(link: str):
    print("Playing", link)
    stop_audio()
    p = Popen(
        ["mpv", "--no-video", link], stdout=TemporaryFile(), stderr=TemporaryFile()
    )


def main() -> None:
    ytl = YTLiveService(sys.argv[1])
    change = ytl.listen()
    while 1:
        if ytl.live_link:
            play(ytl.live_link)
        else:
            print("Vtuber not live", ytl.live_link)
        change.wait()
        change.clear()


if __name__ == "__main__":
    try:
        main()
    except (Exception, SystemExit):
        stop_audio()
