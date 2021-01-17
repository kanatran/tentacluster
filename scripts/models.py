from typing import Optional

from pydantic import BaseModel

class TranscriptEvent(BaseModel):
    timestamp: int
    text: str
    translation: Optional[str]
