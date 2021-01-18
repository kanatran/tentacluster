import asyncio
import os
from pprint import pprint
from pathlib import Path
from threading import Thread
from typing import Optional

import translators as ts
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from autoselenium import chrome
from models import TranscriptEvent
from transcribe import *

static = Path(__file__).resolve().parent / "../web"

app = FastAPI()
app.mount("/static", StaticFiles(directory=static), name="static")

translate = ts.bing


async def translate(jap: str) -> Optional[str]:
    if 0:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: ts.bing(jap))
    return None


def launch_selenium():
    global web  # Avoid garbage collection
    chrome.setup_driver()
    web = chrome.get_selenium(True)
    try:
        web.switch_to.window("1")
    except Exception:
        pass
    web.get("http://localhost:42069/static/index.html")


@app.post("/transcript")
async def transcript_event(transcript: TranscriptEvent):
    print("Got transcript:", transcript.text)
    print("At time:", transcript.timestamp)
    print("Browser translation:", transcript.translation)
    loop = asyncio.get_event_loop()
    write_transcripts(
        "testvideoid",
        transcript.text,
        transcript.translation,
        transcript.srtTime,
        transcript.index,
    )
    # write_transcripts('testvideo', 'test transcript', 'テスト翻訳', ['00:00:00,000', '00:00:01,000'], 1)
    # print("Bing translation:", await translate(transcript.text))
    return 200


@app.get("/")
async def root():
    return {"message": "Hello World"}


# print(translate("どこに向かわれてるんですかや屋号屋号どこどこに入ってるあの値段で家53って言いたいんだけどあの屋号から直々にさん付けやめてくださいみたいなあの呼び捨てにしてくださいって言うね昔言われたんで屋号と言ってます0口で開封配信とかしてほしいねもしかして自分が vtuber になるために作った組織なんでそんなどうしようも色々あのホロライブプロダクションの中にホロライブホロスターズサンスターで3とかあるんだけどちょっとどうしたんやね"))

Thread(target=launch_selenium, daemon=True).start()
