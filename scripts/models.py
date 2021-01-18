from typing import Optional, List

from pydantic import BaseModel


class TranscriptEvent(BaseModel):
    timestamp: int
    text: str
    translation: Optional[str]
    srtTime: List[str]
    index: int
