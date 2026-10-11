import pytest
from app.core.orchestrator import ConversationOrchestrator
from app.domain.schemas import TurnRequest, TurnStatus
from tests.mocks import MockLLMAdapter, MockVoiceAdapter, MockSTTAdapter


@pytest.mark.asyncio
async def test_successful_turn_with_audio():
    mock_llm = MockLLMAdapter(canned_response="It feels wonderful to connect.")
    mock_voice = MockVoiceAdapter()
    mock_stt = MockSTTAdapter()
    orch = ConversationOrchestrator(
        llm_provider=mock_llm,
        voice_provider=mock_voice,
        stt_provider=mock_stt
    )

    req = TurnRequest(message="Hello Samantha", response_mode="text_and_audio")
    res = await orch.execute_turn("session-123", req)

    assert res.status == TurnStatus.COMPLETED
    assert res.assistant_text == "It feels wonderful to connect."
    assert res.audio is not None
    assert res.audio.status == "ready"
    assert res.audio.audio_base64 is not None
    assert mock_voice.synthesized_texts == ["It feels wonderful to connect."]


@pytest.mark.asyncio
async def test_speech_to_speech_audio_turn():
    mock_llm = MockLLMAdapter(canned_response="I heard your voice.")
    mock_voice = MockVoiceAdapter()
    mock_stt = MockSTTAdapter(transcript="What time is it?")
    orch = ConversationOrchestrator(
        llm_provider=mock_llm,
        voice_provider=mock_voice,
        stt_provider=mock_stt
    )

    dummy_audio = b"fake_recorded_voice_bytes"
    res = await orch.execute_audio_turn("session-speech", dummy_audio)

    assert res.status == TurnStatus.COMPLETED
    assert res.user_message == "What time is it?"
    assert res.assistant_text == "I heard your voice."
    assert res.audio.status == "ready"
    assert len(mock_stt.recorded_audios) == 1


@pytest.mark.asyncio
async def test_session_continuity():
    mock_llm = MockLLMAdapter(canned_response="Understood.")
    mock_voice = MockVoiceAdapter()
    mock_stt = MockSTTAdapter()
    orch = ConversationOrchestrator(
        llm_provider=mock_llm,
        voice_provider=mock_voice,
        stt_provider=mock_stt
    )

    await orch.execute_turn("conv-abc", TurnRequest(message="Turn one", response_mode="text_only"))
    await orch.execute_turn("conv-abc", TurnRequest(message="Turn two", response_mode="text_only"))

    session = orch.get_or_create_session("conv-abc")
    assert len(session) == 4
    assert session[0].content == "Turn one"
    assert session[1].content == "Understood."
    assert session[2].content == "Turn two"


@pytest.mark.asyncio
async def test_tts_failure_does_not_break_text_response():
    mock_llm = MockLLMAdapter(canned_response="Text should survive audio failure.")
    mock_voice = MockVoiceAdapter(should_fail=True)
    mock_stt = MockSTTAdapter()
    orch = ConversationOrchestrator(
        llm_provider=mock_llm,
        voice_provider=mock_voice,
        stt_provider=mock_stt
    )

    res = await orch.execute_turn("conv-tts-fail", TurnRequest(message="Hello", response_mode="text_and_audio"))
    assert res.status == TurnStatus.COMPLETED
    assert res.assistant_text == "Text should survive audio failure."
    assert res.audio.status == "unavailable"
