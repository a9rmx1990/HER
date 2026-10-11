from abc import ABC, abstractmethod
from typing import List
from app.domain.schemas import Message


class LLMProvider(ABC):
    @abstractmethod
    async def generate_response(
        self,
        messages: List[Message],
        system_instruction: str = ""
    ) -> str:
        """Generate response text given message history and system instruction."""
        pass


class VoiceProvider(ABC):
    @abstractmethod
    async def synthesize_speech(
        self,
        text: str,
        voice_id: str = "",
        model_id: str = ""
    ) -> bytes:
        """Synthesize text to audio bytes."""
        pass
