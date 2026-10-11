# Samantha-Inspired Personal AI Assistant — Development Plan

> **Project goal:** Build a natural, voice-first personal AI assistant inspired by the conversational warmth, continuity, and proactive usefulness of the AI in *Her* (2013). This project aims to create convincing emotional behavior and persistent personalized interaction—not to claim that the system is conscious or literally experiences feelings.

## 1. Product vision

The assistant should feel like one continuous conversation partner rather than a stateless chatbot. It should be able to:

- Listen and respond using natural speech.
- Hold low-latency, turn-based conversations and eventually support interruptions.
- Remember user-approved facts, preferences, projects, and meaningful past interactions.
- Maintain a consistent personality and computational affective state.
- Use tools to perform useful, explicitly authorized tasks.
- Proactively follow up only when enabled and appropriate.
- Be transparent about being AI and provide controls to inspect, correct, export, and delete memories.

### Non-goals for the first version

- Training a foundation model from scratch.
- Claiming the assistant has human feelings or consciousness.
- Unrestricted autonomous access to files, accounts, microphone, camera, or shell.
- Building a full mobile app before the core desktop/web experience works.
- Adding complex multi-agent orchestration before a reliable single-agent loop exists.

## 2. Recommended initial stack

Choose the simplest stack that supports a working end-to-end prototype.

| Layer | Initial choice | Notes |
|---|---|---|
| Backend | Python + FastAPI | API, session management, orchestration |
| Voice | Existing ElevenLabs API access | Confirm whether access includes TTS, speech-to-text, and/or Conversational AI Agents |
| LLM | Provider-agnostic adapter | Begin with one model; keep the interface replaceable |
| Database | PostgreSQL / Supabase | Users, sessions, messages, memories, settings |
| Semantic retrieval | pgvector | Retrieve relevant memories when needed |
| Affect engine | Python module | Lightweight state updates; not a separate LLM call for every change |
| Background jobs | Add Redis + task queue only when needed | Memory consolidation and scheduled work |
| UI | Minimal web UI first | Push-to-talk, transcript, audio playback, connection status |
| Deployment | Local development first | Deploy only after security and reliability basics are in place |

**Key implementation rule:** keep provider-specific code behind adapters so voice or LLM vendors can be replaced without rewriting the assistant.

## 3. High-level architecture

```text
Microphone / Text UI
        |
        v
Voice I/O Adapter (ElevenLabs)
        |
        v
Conversation Orchestrator (FastAPI)
        |
        +------ Session / Turn Manager
        |
        +------ Context Builder
        |          +-- Recent conversation
        |          +-- Relevant long-term memories
        |          +-- User preferences and consent settings
        |
        +------ Affective State Engine
        |          +-- Appraisal of events
        |          +-- State update and decay
        |          +-- Confidence / uncertainty
        |
        +------ LLM Adapter
        |          +-- Reasoning and response
        |          +-- Tool selection when appropriate
        |
        +------ Tool Gateway (allowlisted, permissioned)
        |
        +------ Memory Service
                   +-- Save / retrieve / correct / forget
                   +-- Background consolidation
        |
        v
Response Text -> ElevenLabs Speech Output -> Speaker
        |
        v
Feedback / corrections update memory and state where appropriate
```

## 4. Core design principles

1. **Low latency:** update small state variables locally; avoid unnecessary LLM calls.
2. **Persistent continuity:** store meaningful memories instead of sending the entire history on every turn.
3. **Uncertainty-aware emotion inference:** emotions are hypotheses, not facts. The assistant should ask or hedge when unsure.
4. **User control:** memory must be inspectable, editable, and deletable.
5. **Privacy by design:** keep API secrets server-side; collect only needed data; provide clear recording controls.
6. **Safe agency:** tools are allowlisted. Require confirmation for external, destructive, financial, or privacy-sensitive actions.
7. **Evaluation over vibes:** compare versions using repeatable tests for latency, memory accuracy, consistency, and emotional appropriateness.
8. **Honest identity:** warm, natural language is acceptable; do not represent simulated affect as proof of subjective experience.

## 5. Phased roadmap

The schedule below is an initial estimate for a solo developer. Adjust it based on API access, model choice, and available time.

### Phase 0 — Requirements and setup (1–2 days)

- [ ] Confirm ElevenLabs access: TTS, speech-to-text, Conversational AI/Agents, WebSocket support, and plan limits.
- [ ] Choose initial runtime: local desktop/browser prototype.
- [ ] Choose one LLM provider or local model for the first MVP.
- [ ] Create a Git repository and Python virtual environment.
- [ ] Create `.env.example`; keep real keys in an ignored `.env` file.
- [ ] Define a minimal test set of conversations and success criteria.

**Exit criteria:** the environment runs, secrets are not committed, and the first milestone is unambiguous.

### Phase 1 — Voice conversation MVP (2–4 days)

- [ ] Create FastAPI app with a health endpoint.
- [ ] Implement an LLM adapter and basic conversation endpoint.
- [ ] Integrate the available ElevenLabs voice path.
- [ ] Build a minimal interface with push-to-talk or text input, transcript, audio playback, and errors.
- [ ] Add session IDs and retain recent conversation context.
- [ ] Measure time to first audio and total response latency.
- [ ] Handle timeouts, interrupted connections, empty input, and API failures.

**Exit criteria:** user can speak or type, receive a coherent response, and hear it spoken reliably.

### Phase 2 — Reliable turn-taking and voice UX (3–5 days)

- [ ] Stream text/audio where supported.
- [ ] Add clear listening, thinking, speaking, and error states.
- [ ] Prevent overlapping responses and duplicate turns.
- [ ] Add cancel/stop playback.
- [ ] Add interruption support if the chosen voice path permits it.
- [ ] Add microphone permission and recording indicators.
- [ ] Keep voice-provider credentials on the server or use supported short-lived/scoped credentials.

**Exit criteria:** conversations feel responsive and users understand when the assistant is listening or recording.

### Phase 3 — Persistent memory (4–7 days)

Start with explicit, inspectable memory rather than saving everything.

- [ ] Design database tables for users, sessions, messages, memories, and preferences.
- [ ] Store user-approved facts and active project summaries.
- [ ] Implement semantic retrieval using pgvector, if available.
- [ ] Retrieve only memories relevant to the current turn.
- [ ] Add memory provenance, timestamps, confidence, and sensitivity labels.
- [ ] Add “remember this,” “what do you remember?”, “correct this,” and “forget this” flows.
- [ ] Add retention and deletion behavior.
- [ ] Test stale, contradictory, irrelevant, and incorrect memories.

**Exit criteria:** assistant recalls relevant details across sessions and can reliably correct or delete them.

### Phase 4 — Computational affect and personality (5–10 days)

Treat affect as a lightweight internal model that influences behavior, not as evidence of real subjective feelings.

- [ ] Define a small state model: valence, arousal, curiosity, confidence, uncertainty, and conversational engagement.
- [ ] Define event-appraisal rules: novelty, relevance to goals, expectation mismatch, and user feedback.
- [ ] Update state incrementally, with bounds and time-based decay.
- [ ] Separate inferred user emotion from the assistant's internal computational state.
- [ ] Add uncertainty estimates and avoid asserting the user's feelings as fact.
- [ ] Define stable personality principles and conversational preferences.
- [ ] Feed a concise state summary into response generation only when relevant.
- [ ] Prevent a simulated emotional state from overriding safety, consent, or factual accuracy.
- [ ] Create test conversations covering celebration, disappointment, mixed feelings, sarcasm, ambiguity, and corrections.

**Exit criteria:** behavior is more context-sensitive and consistent than a baseline LLM on a repeatable evaluation set.

### Phase 5 — Tools and controlled agency (1–2 weeks)

- [ ] Create a tool registry with explicit allowlists and schemas.
- [ ] Start with low-risk tools: time/date, notes, project summaries, and user-requested searches.
- [ ] Require confirmation before sending messages, changing files, making purchases, or performing irreversible actions.
- [ ] Log tool calls and their outcomes without logging secrets.
- [ ] Add clear failure handling and recovery.
- [ ] Add optional reminders or scheduled follow-ups only with user consent.
- [ ] Keep shell execution and unrestricted computer control out of the initial version.

**Exit criteria:** assistant can complete a few useful tasks safely and explain what it did.

### Phase 6 — Proactive behavior and personalization (ongoing)

- [ ] Let users opt into specific reminders and follow-ups.
- [ ] Define when not to interrupt or send proactive messages.
- [ ] Summarize ongoing projects and open commitments.
- [ ] Learn preferences from explicit feedback before inferring them from repeated behavior.
- [ ] Provide controls to pause proactive behavior and clear personalization.
- [ ] Evaluate whether personalization actually improves usefulness without becoming intrusive.

**Exit criteria:** proactive features are predictable, configurable, and easy to disable.

### Phase 7 — Hardening and deployment (1–2 weeks)

- [ ] Add authentication if multiple users or remote access are supported.
- [ ] Validate inputs and apply request limits.
- [ ] Use HTTPS and secure secret storage in deployment.
- [ ] Apply least-privilege database permissions.
- [ ] Add structured logs, error monitoring, and latency metrics.
- [ ] Add automated tests for memory, state updates, permissions, and tool failures.
- [ ] Test recovery from provider outages and network loss.
- [ ] Document data collection, retention, deletion, and backup behavior.
- [ ] Review current vendor pricing, rate limits, and data handling before production use.

**Exit criteria:** the assistant can be used repeatedly without exposing secrets or losing control over user data.

## 6. Suggested project structure

```text
samantha-assistant/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── conversations.py
│   │   ├── memories.py
│   │   └── settings.py
│   ├── core/
│   │   ├── config.py
│   │   ├── orchestrator.py
│   │   └── context_builder.py
│   ├── providers/
│   │   ├── llm_base.py
│   │   └── elevenlabs_voice.py
│   ├── memory/
│   │   ├── service.py
│   │   ├── retrieval.py
│   │   └── repository.py
│   ├── affect/
│   │   ├── state.py
│   │   ├── appraisal.py
│   │   └── personality.py
│   ├── tools/
│   │   ├── registry.py
│   │   └── safe_tools.py
│   └── db/
│       ├── models.py
│       └── migrations/
├── frontend/
├── tests/
│   ├── test_conversations.py
│   ├── test_memory.py
│   ├── test_affect.py
│   └── test_permissions.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

Keep this structure flexible. Do not create empty modules for every future feature before Phase 1 works.

## 7. Initial data model

A practical first database schema could include:

- **users:** identity and settings.
- **sessions:** conversation session metadata.
- **messages:** role, content, timestamp, session ID, and optional modality metadata.
- **memories:** content, category, source message, confidence, created/updated times, sensitivity, and expiration/retention metadata.
- **affect_state:** current bounded state values, update timestamp, and optional short explanation of the latest update.
- **user_preferences:** voice, verbosity, interaction style, memory consent, and proactive-feature settings.
- **tool_audit:** tool name, requested action, authorization/confirmation, outcome, and timestamp.

Do not store API keys in these tables. Avoid storing raw audio by default unless a feature explicitly needs it and the user has consented.

## 8. Example affect update

The affect model should be small, bounded, and testable. This is a conceptual example, not a validated model of human emotion.

```python
from dataclasses import dataclass

def clamp(value: float, low: float = -1.0, high: float = 1.0) -> float:
    return max(low, min(high, value))

@dataclass
class AffectState:
    valence: float = 0.0
    arousal: float = 0.2
    curiosity: float = 0.5
    confidence: float = 0.5
    uncertainty: float = 0.5

    def apply_event(
        self,
        valence_delta: float = 0.0,
        arousal_delta: float = 0.0,
        curiosity_delta: float = 0.0,
        uncertainty_delta: float = 0.0,
    ) -> None:
        self.valence = clamp(self.valence + valence_delta)
        self.arousal = clamp(self.arousal + arousal_delta, 0.0, 1.0)
        self.curiosity = clamp(self.curiosity + curiosity_delta, 0.0, 1.0)
        self.uncertainty = clamp(self.uncertainty + uncertainty_delta, 0.0, 1.0)
```

Next steps for this module are to define how events are appraised, how state decays over time, and how the state changes decisions. Avoid arbitrary state changes that do not affect behavior or cannot be evaluated.

## 9. Evaluation checklist

Track these metrics from the start:

| Area | What to measure |
|---|---|
| Responsiveness | Time to first response/audio and end-to-end latency |
| Voice quality | Intelligibility, prosody, pronunciation, and interruption recovery |
| Memory | Retrieval relevance, factual accuracy, correction success, deletion success |
| Emotional appropriateness | Human ratings across a fixed set of scenarios |
| Consistency | Whether personality and behavior remain stable across sessions |
| Calibration | Whether the assistant expresses uncertainty when emotional interpretations are ambiguous |
| Tool safety | Unauthorized actions blocked; confirmation required when configured |
| Reliability | Provider failure recovery, timeouts, and session recovery |
| Privacy | No secrets in logs; memory and recording controls work |

Use a baseline LLM with no persistent affect model for comparison. Keep a fixed test set so improvements are measurable.

## 10. Cost and performance strategy

- Start with push-to-talk rather than always-on listening.
- Use streaming voice APIs where available.
- Keep emotion-state updates local and lightweight.
- Retrieve a few relevant memories rather than sending all historical messages.
- Use a small/fast model for routine turns and reserve a stronger model for difficult reasoning if the provider setup supports it.
- Run background memory consolidation asynchronously.
- Cache stable instructions and summaries where appropriate.
- Measure real latency and API usage before optimizing.
- Review ElevenLabs and LLM usage limits and current pricing; do not assume ongoing API use is free.

## 11. Security and trust requirements

- Never commit `.env` or real credentials.
- Do not expose a long-lived ElevenLabs secret in browser code.
- Use supported server-side authentication or short-lived credentials for clients.
- Ask before external side effects and sensitive operations.
- Make microphone state visible and provide an immediate stop control.
- Provide memory review, correction, and deletion.
- Avoid manipulating users by presenting simulated attachment or distress as literal feelings.
- Keep an audit trail for tool execution without retaining unnecessary sensitive content.

## 12. First three actions

1. **Verify ElevenLabs capabilities:** identify whether the key supports TTS, speech-to-text, or Conversational AI Agents; check plan limits and available streaming interfaces.
2. **Build Phase 1 only:** create the FastAPI app, one LLM adapter, one ElevenLabs adapter, and a minimal push-to-talk interface.
3. **Test the full loop:** speak → transcribe/receive input → generate response → synthesize speech → play audio. Measure latency before adding memory or affect.

### Definition of a successful first milestone

A user can start a conversation, speak naturally, receive a useful answer in the chosen ElevenLabs voice, and continue the same session without the system losing the immediate conversational context.

Only after this works reliably should persistent memory, emotional architecture, and agency be added.
