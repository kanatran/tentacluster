import asyncio
import os
import subprocess
from pathlib import Path
from typing import List

static = Path(__file__).resolve().parent


async def aio_write_transcripts(video, transcript, translation, srtTimes):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, lambda: write_transcripts(video, transcript, translation, srtTimes)
    )


def write_transcripts(
    video: str, transcript: str, translation: str, srtTimes: List[str]
):
    subprocess.call(["sh", f"{static}/checkout.sh", video])

    time = f"{srtTimes[0]} --> {srtTimes[1]}"

    paths = [
        f"{static}/../../baquap/transcript.srt",
        f"{static}/../../baquap/tl_transcript.srt",
        f"{static}/../../baquap/last_tl.txt",
    ]

    if not os.path.exists(paths[2]):
        index = 1
    else:
        with open(paths[2]) as f:
            index = int(f.readline()) + 1

    texts = [
        f"""{index}
{time}
{transcript}

""",
        f"""{index}
{time}
{translation}

""",
        f"""{index}
{time}
{transcript}
{translation}

""",
    ]

    with open(paths[0], "a+") as f:
        f.write(texts[0])

    with open(paths[1], "a+") as f:
        f.write(texts[1])

    with open(paths[2], "w+") as f:
        f.write(texts[2])

    subprocess.call(["sh", f"{static}/commit.sh", video])
