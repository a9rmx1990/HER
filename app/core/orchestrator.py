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

    async def execute_turn(
        self,
        conversation_id: str,
        request: TurnRequest
    ) -> TurnResponse:
        turn_id = str(uuid.uuid4())
        history = self.get_or_create_session(conversation_id)

        # 1. Append user message to bounded history
        user_msg = Message(role=Role.USER, content=request.message.strip())
        history.append(user_msg)

        # Keep a bounded context window of recent messages
        context_messages = history[-10:]

        # 2. Call LLM
        try:
            assistant_text = await self.llm.generate_response(
                messages=context_messages,
                system_instruction=SAMANTHA_SYSTEM_PROMPT
            )
        except Exception as e:
            return TurnResponse(
                turn_id=turn_id,
                conversation_id=conversation_id,
                status=TurnStatus.FAILED,
                user_message=request.message,
                assistant_text="",
                error=f"LLM failure: {str(e)}"
            )

        # Append assistant response to history
        history.append(Message(role=Role.ASSISTANT, content=assistant_text))

        # 3. Synthesize voice if requested
        audio_info = AudioInfo(status="unavailable")
        if request.response_mode == "text_and_audio":
            try:
                audio_bytes = await self.voice.synthesize_speech(text=assistant_text)
                audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
                audio_info = AudioInfo(
                    status="ready",
                    content_type="audio/mpeg",
                    audio_base64=audio_base64
                )
            except Exception as e:
                audio_info = AudioInfo(
                    status="unavailable",
                    content_type="audio/mpeg"
                )

        return TurnResponse(
            turn_id=turn_id,
            conversation_id=conversation_id,
            status=TurnStatus.COMPLETED,
            user_message=request.message,
            assistant_text=assistant_text,
            audio=audio_info
        )
