import httpx
from app.providers.base import VoiceProvider


class ElevenLabsVoiceAdapter(VoiceProvider):
    def __init__(
        self,
        api_key: str,
        default_voice_id: str = "EXAVITQu4vr4xnSDxMaL",
        default_model_id: str = "eleven_flash_v2_5"
    ):
        self.api_key = api_key
        self.default_voice_id = default_voice_id
        self.default_model_id = default_model_id

    async def synthesize_speech(
        self,
        text: str,
        voice_id: str = "",
        model_id: str = ""
    ) -> bytes:
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY is not configured.")

        selected_voice = voice_id or self.default_voice_id
        selected_model = model_id or self.default_model_id

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{selected_voice}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model_id": selected_model,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code != 200:
                raise RuntimeError(
                    f"ElevenLabs TTS error ({resp.status_code}): {resp.text[:200]}"
                )
            return resp.content

    async def transcribe_audio(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        content_type: str = "audio/wav"
    ) -> str:
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY is not configured.")

        url = "https://api.elevenlabs.io/v1/speech-to-text"
        headers = {"xi-api-key": self.api_key}
        files = {"file": (filename, audio_bytes, content_type)}
        data = {"model_id": "scribe_v1"}

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, headers=headers, files=files, data=data)
            if resp.status_code != 200:
                raise RuntimeError(
                    f"ElevenLabs STT error ({resp.status_code}): {resp.text[:200]}"
                )
            result = resp.json()
            return result.get("text", "").strip()
