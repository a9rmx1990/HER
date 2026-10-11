import httpx
from app.providers.base import VoiceProvider, SpeechToTextProvider


class ElevenLabsVoiceAdapter(VoiceProvider, SpeechToTextProvider):
    def __init__(
        self,
        api_key: str,
        default_voice_id: str = "EXAVITQu4vr4xnSDxMaL",
        default_model_id: str = "eleven_flash_v2_5"
    ):
        self.api_key = api_key
        self.voice_id = default_voice_id
        self.model_id = default_model_id
        self.base_url = "https://api.elevenlabs.io/v1"

    async def synthesize_speech(
        self,
        text: str,
        voice_id: str = "",
        model_id: str = ""
    ) -> bytes:
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY is not configured.")

        selected_voice = voice_id or self.voice_id
        selected_model = model_id or self.model_id
        url = f"{self.base_url}/text-to-speech/{selected_voice}"

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
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code != 200:
                raise RuntimeError(
                    f"ElevenLabs TTS failed: {response.status_code} - {response.text}"
                )
            return response.content
