from typing import List
from app.domain.schemas import Message
from app.providers.base import LLMProvider, VoiceProvider


class MockLLMAdapter(LLMProvider):
    def __init__(self, canned_response: str = "I am here with you."):
        self.canned_response = canned_response
        self.received_messages: List[Message] = []

    async def generate_response(
        self,
        messages: List[Message],
        system_instruction: str = ""
    ) -> str:
        self.received_messages = list(messages)
        return self.canned_response


class MockVoiceAdapter(VoiceProvider):
    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail
        self.synthesized_texts: List[str] = []

    async def synthesize_speech(
        self,
        text: str,
        voice_id: str = "",
        model_id: str = ""
    ) -> bytes:
        if self.should_fail:
            raise RuntimeError("Mock audio synthesis failure")
        self.synthesized_texts.append(text)
        return b"ID3_MOCK_AUDIO_DATA"


class MockSTTAdapter:
    def __init__(self, transcript: str = "Test transcript", should_fail: bool = False):
        self.transcript = transcript
        self.should_fail = should_fail
        self.recorded_audios = []

    async def transcribe_audio(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        content_type: str = "audio/wav"
    ) -> str:
        if self.should_fail:
            raise RuntimeError("Mock STT transcription failure")
        self.recorded_audios.append(audio_bytes)
        return self.transcript
