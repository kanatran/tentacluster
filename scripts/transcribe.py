import os
import subprocess
from pathlib import Path

static = Path(__file__).resolve().parent


def write_transcripts(video, transcript, translation, srtTimes, index):
    subprocess.call(["sh", f"{static}/checkout.sh", video])

    time = f"{srtTimes[0]} --> {srtTimes[1]}"

    texts = [
        f"""
{index}
{time}
{transcript}
""",
        f"""
{index}
{time}
{translation}
""",
        f"""
{time}
{transcript}
{translation}
""",
    ]

    paths = [
        f"{static}/../../baquap/transcript.srt",
        f"{static}/../../baquap/tl_transcript.srt",
        f"{static}/../../baquap/last_tl.txt",
    ]


    with open(paths[0], "a+") as f:
        f.write(texts[0])

    with open(paths[1], "a+") as f:
        f.write(texts[1])

    with open(paths[2], "w+") as f:
        f.write(texts[2])

    subprocess.call(["sh", f"{static}/commit.sh", video])
