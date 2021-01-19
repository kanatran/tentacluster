from typing import List, Optional

from pydantic import BaseModel


class TranscriptEvent(BaseModel):
    timestamp: int
    text: str
    translation: Optional[str]
    srtTime: List[str]
    tlIndex: int
