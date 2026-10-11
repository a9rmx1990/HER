import base64
import uuid
from typing import Dict, List
from app.providers.base import LLMProvider, VoiceProvider, SpeechToTextProvider
from app.domain.schemas import (
    TurnRequest,
    TurnResponse,
    TurnStatus,
    AudioInfo,
    Message,
    Role
)
from app.core.prompts import SAMANTHA_SYSTEM_PROMPT


class ConversationOrchestrator:
    def __init__(
        self,
        llm_provider: LLMProvider,
        voice_provider: VoiceProvider,
        stt_provider: SpeechToTextProvider
    ):
        self.llm = llm_provider
        self.voice = voice_provider
        self.stt = stt_provider
        self.sessions: Dict[str, List[Message]] = {}

    def get_or_create_session(self, conversation_id: str) -> List[Message]:
        if conversation_id not in self.sessions:
            self.sessions[conversation_id] = []
        return self.sessions[conversation_id]
