# HER — Voice-First Personal AI Assistant

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![LLM](https://img.shields.io/badge/LLM-Gemini_3.8_Flash-4285F4.svg)](https://ai.google.dev/)
[![Voice](https://img.shields.io/badge/Voice-ElevenLabs_Flash_v2.5-black.svg)](https://elevenlabs.io/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> *"I'm here with you."*

**HER** is an open-source, voice-first personal AI assistant inspired by the conversational warmth, emotional perceptiveness, and intellectual continuity of Samantha in Spike Jonze's *Her* (2013).

Built on a modular **Ports & Adapters (Hexagonal)** architecture, HER coordinates low-latency speech transcription (ElevenLabs Scribe STT), adaptive conversational reasoning (Google Gemini 3.8 Flash), and expressive voice synthesis (ElevenLabs Flash v2.5) into a unified, fluid speech-to-speech interaction loop.

---

## Key Features

- **Fluid Speech-to-Speech (S2S):** Native browser audio capture via Web Audio MediaRecorder, server-side transcription, LLM reasoning, and sub-second voice synthesis delivered as streaming base64 audio.
- **Samantha Persona & Affective Alignment:** Behavioral guidelines grounded in empathy, curiosity, intellectual depth, honest disclosure of AI identity, and transparent uncertainty calibration.
- **Ports & Adapters (Hexagonal Architecture):** LLM, STT, and TTS engines are completely isolated behind abstract provider interfaces (`LLMProvider`, `VoiceProvider`, `SpeechToTextProvider`). Swap Gemini for Claude, OpenAI, or local Ollama; or ElevenLabs for Whisper, Deepgram, or Cartesia without rewriting core orchestrator logic.
- **Zero-Secret Leakage Guarantee:** All API credentials remain strictly server-side. No API keys or external vendor tokens are exposed to client-side assets.
- **Graceful Degradation:** If audio synthesis or network spikes occur, the conversational text transcript survives and is delivered without failing the turn.
- **Full Test Harness:** Comprehensive mock adapters and automated unit tests for turn orchestration, audio pipelines, session continuity, and health endpoints.
- **Modern Glassmorphic Web Client:** Voice-first web interface featuring push-to-talk, audio waveform visualizer, conversation transcript logs, and responsive controls.

---

## High-Level Architecture

```text
Microphone / Audio UI
        │
        ▼ (multipart audio/webm)
Presentation Layer (FastAPI API Router)
        │
        ▼
Conversation Orchestrator
        ├── STT Adapter (ElevenLabs Scribe STT)
        ├── Context Builder & Session History
        ├── Behavioral Prompt Engine (Samantha SKILL.md)
        ├── LLM Adapter (Google Gemini 3.8 Flash)
        └── TTS Adapter (ElevenLabs Flash v2.5 Voice Synthesis)
        │
        ▼ (TurnResponse with transcript, text & audio bytes)
Web Client (Browser Audio Playback & Transcript View)
```

---

## Project Structure

```text
.
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── conversations.py       # REST API endpoints (sessions, text/audio turns)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Pydantic Settings & environment validation
│   │   ├── orchestrator.py        # Turn orchestration & session lifecycle
│   │   └── prompts.py             # Samantha persona & behavioral system prompts
│   ├── domain/
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic domain models (Message, TurnRequest, etc.)
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py                # Abstract provider ports (LLM, Voice, STT)
│   │   ├── elevenlabs.py          # ElevenLabs STT & TTS concrete adapter
│   │   └── gemini.py              # Google Gemini LLM adapter with backoff
│   └── main.py                    # FastAPI application factory & static mount
├── docs/
│   ├── AGENT.md                   # Operational guidelines & safety guardrails
│   ├── architecture.md            # Comprehensive system architecture & dataflows
│   ├── plan.md                    # Product vision & phased development roadmap
│   └── SKILL.md                   # Samantha conversational persona specifications
├── static/
│   └── index.html                 # Voice-first client UI with waveform visualizer
├── tests/
│   ├── mocks.py                   # Mock providers for deterministic testing
│   └── test_conversations.py      # Unit and integration test suite
├── arch0.md                       # Current implementation status (Phase 0 & 1)
├── pyproject.toml                 # Packaging & dependencies
└── .env.example                   # Environment configuration template
```

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- [Google AI Studio API Key](https://aistudio.google.com/) (Gemini)
- [ElevenLabs API Key](https://elevenlabs.io/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/a9rmx1990/HER.git
   cd HER
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Open `.env` and set your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL   # Bella (or any voice ID)
   ELEVENLABS_MODEL_ID=eleven_flash_v2_5
   ```

---

## Running the Application

Start the development server with Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **Web Client:** Open [http://localhost:8000](http://localhost:8000) in your browser.
- **Interactive API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Checks:**
  - Liveness: `GET /health/live`
  - Readiness: `GET /health/ready`

---

## Running Tests

Execute the automated test suite with pytest:

```bash
pytest
```

---

## API Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health/live` | Liveness probe returning basic health status |
| `GET` | `/health/ready` | Readiness probe verifying provider configurations |
| `POST` | `/api/v1/conversations` | Initialize a new conversational session |
| `POST` | `/api/v1/conversations/{id}/turns` | Submit a text turn (supports text or audio output) |
| `POST` | `/api/v1/conversations/{id}/audio-turns` | Upload recorded audio turn for STT → LLM → TTS pipeline |

---

## Roadmap

- [x] **Phase 0:** Requirements, provider integration, and project foundation.
- [x] **Phase 1:** End-to-end Speech-to-Speech (S2S) MVP with FastAPI, Gemini, and ElevenLabs.
- [ ] **Phase 2:** Low-latency WebSocket streaming for real-time turn interruption and token-by-token audio.
- [ ] **Phase 3:** Long-term memory persistence with PostgreSQL and pgvector semantic retrieval.
- [ ] **Phase 4:** Computational affect engine (bounded state updates for valence, arousal, curiosity, and uncertainty).
- [ ] **Phase 5:** Permissioned tool execution gateway with user confirmation safeguards.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
