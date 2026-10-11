from typing import List
import httpx
from app.providers.base import LLMProvider
from app.domain.schemas import Message, Role


class GeminiLLMAdapter(LLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.api_key = api_key
        self.model = model
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

    async def generate_response(
        self,
        messages: List[Message],
        system_instruction: str = ""
    ) -> str:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        contents = []
        for msg in messages:
            role = "user" if msg.role == Role.USER else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg.content}]
            })

        payload = {"contents": contents}

        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        async with httpx.AsyncClient(timeout=30.0) as client:
            last_err = None
            for attempt in range(3):
                try:
                    resp = await client.post(self.endpoint, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        candidates = data.get("candidates", [])
                        if not candidates:
                            raise RuntimeError("No candidate responses returned by Gemini.")

                        parts = candidates[0].get("content", {}).get("parts", [])
                        text_response = "".join(p.get("text", "") for p in parts)
                        return text_response.strip()

                    # Check if retryable (503, 429)
                    if resp.status_code in (429, 503):
                        import asyncio
                        await asyncio.sleep(1.0 * (attempt + 1))
                        last_err = RuntimeError(f"Gemini API error ({resp.status_code}): {resp.text[:200]}")
                        continue
                    else:
                        raise RuntimeError(f"Gemini API error ({resp.status_code}): {resp.text[:200]}")
                except (httpx.TimeoutException, httpx.NetworkError) as net_err:
                    import asyncio
                    await asyncio.sleep(1.0 * (attempt + 1))
                    last_err = net_err

            raise last_err or RuntimeError("Gemini request failed after retries.")
