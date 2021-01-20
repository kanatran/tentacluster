"""
python run_audio.py channel_id
"""

from subprocess import PIPE, Popen
import sys

from yt import YTLiveService

processes = list()


def stop_audio():
    for p in processes:
        p.terminate()


def play(link: str):
    print("Playing", link)
    stop_audio()
    processes.append(Popen(["mpv", "--no-video", link], stdout=PIPE, stderr=PIPE,))


def main() -> None:
    ytl = YTLiveService(sys.argv[1])
    change = ytl.listen()
    while 1:
        if ytl.live_link:
            play(ytl.live_link)
        else:
            print("Vtuber not live anymore")
        change.wait()
        change.clear()


if __name__ == "__main__":
    try:
        main()
    except (Exception, SystemExit):
        stop_audio()
