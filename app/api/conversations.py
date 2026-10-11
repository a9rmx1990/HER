import uuid
from typing import Dict
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from app.domain.schemas import TurnRequest, TurnResponse
from app.core.orchestrator import ConversationOrchestrator
from app.providers.gemini import GeminiLLMAdapter
from app.providers.elevenlabs import ElevenLabsVoiceAdapter
from app.core.config import settings

router = APIRouter(prefix="/api/v1", tags=["Conversations"])

eleven_adapter = ElevenLabsVoiceAdapter(
    api_key=settings.ELEVENLABS_API_KEY,
    default_voice_id=settings.ELEVENLABS_VOICE_ID,
    default_model_id=settings.ELEVENLABS_MODEL_ID
)

_orchestrator = ConversationOrchestrator(
    llm_provider=GeminiLLMAdapter(
        api_key=settings.GEMINI_API_KEY,
        model=settings.GEMINI_MODEL
    ),
    voice_provider=eleven_adapter,
    stt_provider=eleven_adapter
)


def get_orchestrator() -> ConversationOrchestrator:
    return _orchestrator


class ConversationCreateResponse(BaseModel):
    conversation_id: str


@router.post("/conversations", response_model=ConversationCreateResponse)
async def create_conversation():
    cid = str(uuid.uuid4())
    _orchestrator.get_or_create_session(cid)
    return ConversationCreateResponse(conversation_id=cid)


@router.post("/conversations/{conversation_id}/turns", response_model=TurnResponse)
async def submit_turn(
    conversation_id: str,
    request: TurnRequest,
    orch: ConversationOrchestrator = Depends(get_orchestrator)
):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty.")
    
    result = await orch.execute_turn(conversation_id, request)
    return result


@router.post("/conversations/{conversation_id}/audio-turns", response_model=TurnResponse)
async def submit_audio_turn(
    conversation_id: str,
    audio: UploadFile = File(...),
    orch: ConversationOrchestrator = Depends(get_orchestrator)
):
    audio_bytes = await audio.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Audio payload is empty.")

    filename = audio.filename or "audio.webm"
    content_type = audio.content_type or "audio/webm"

    result = await orch.execute_audio_turn(
        conversation_id=conversation_id,
        audio_bytes=audio_bytes,
        filename=filename,
        content_type=content_type
    )
    return result
