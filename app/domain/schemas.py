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


class TurnRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User input text or transcript")
    response_mode: str = Field(default="text_and_audio", description="'text_only' or 'text_and_audio'")


class TurnResponse(BaseModel):
    turn_id: str
    conversation_id: str
    status: TurnStatus
    user_message: str
    assistant_text: str
    audio: Optional[AudioInfo] = None
    error: Optional[str] = None
