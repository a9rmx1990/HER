from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    role: Role
    content: str


class TurnStatus(str, Enum):
    RECEIVED = "received"
    REASONING = "reasoning"
    SYNTHESIZING = "synthesizing"
    COMPLETED = "completed"
    FAILED = "failed"


class AudioInfo(BaseModel):
    status: str = "unavailable"  # "ready" or "unavailable"
    content_type: str = "audio/mpeg"
    audio_base64: Optional[str] = None
