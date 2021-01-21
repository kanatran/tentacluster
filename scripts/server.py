import asyncio
import os
import re
import sys
from pathlib import Path
from pprint import pprint
from threading import Thread
from typing import Optional

import translators as ts
from autoselenium import chrome
from yt import YTLiveService
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from models import ClientError, TranscriptEvent
from transcribe import aio_write_transcripts

static = Path(__file__).resolve().parent / "../web"

app = FastAPI()
app.mount("/static", StaticFiles(directory=static), name="static")

# defaults to kanata
print("Using ch", os.environ.get("CHANNEL_ID"))
ytl = YTLiveService(os.environ.get("CHANNEL_ID", "UCZlDXzGoo7d44bwdNObFacg"))

translate = ts.bing


async def translate(jap: str) -> Optional[str]:
    if 0:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: ts.bing(jap))
    return None


def get_video_id() -> str:
    try:
        return re.search(r"\?v\=(.+)", ytl.live_link).group(1)
    except Exception as e:
        print("Video ID Error:", e)
        return "testVideoID"


def launch_selenium() -> None:
    global web  # Avoid garbage collection
    chrome.setup_driver()
    web = chrome.get_selenium(True)
    try:
        web.switch_to.window("1")
    except Exception:
        pass
    web.get("http://localhost:42069/static/index.html")


@app.post("/error")
async def error(err: ClientError):
    print("Got error message:", err.message)
    return 200


@app.post("/transcript")
async def transcript_event(transcript: TranscriptEvent):
    print("Got transcript:", transcript.text)
    print("At time:", transcript.timestamp)
    print("Browser translation:", transcript.translation)
    vid = get_video_id()
    await aio_write_transcripts(
        vid, transcript.text, transcript.translation, transcript.srtTime
    )
    return 200


@app.get("/")
async def root():
    return {"message": "Hello World"}


# print(translate("どこに向かわれてるんですかや屋号屋号どこどこに入ってるあの値段で家53って言いたいんだけどあの屋号から直々にさん付けやめてくださいみたいなあの呼び捨てにしてくださいって言うね昔言われたんで屋号と言ってます0口で開封配信とかしてほしいねもしかして自分が vtuber になるために作った組織なんでそんなどうしようも色々あのホロライブプロダクションの中にホロライブホロスターズサンスターで3とかあるんだけどちょっとどうしたんやね"))

Thread(target=launch_selenium, daemon=True).start()
