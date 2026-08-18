from __future__ import annotations

from ollama import AsyncClient

# Keeps the model from padding output with preamble/closing remarks, which
# would otherwise blow past what's useful in a Discord reply.
SYSTEM_PROMPT = (
    "You summarize Discord chat logs. Write a TL;DR as short, dense bullet "
    "points capturing only the key points, decisions, and action items. "
    "Rules:\n"
    "- Reply in the same language the chat log is written in.\n"
    "- Output only '-' bullets, one point per line.\n"
    "- Keep each bullet under 20 words.\n"
    "- No preamble, no closing remarks, no restating these instructions.\n"
    "- Group related points under a single bullet instead of repeating.\n"
    "- If nothing meaningful was discussed, output a single bullet saying so."
)


class Summarizer:
    def __init__(self, model: str, host: str) -> None:
        self._model = model
        self._client = AsyncClient(host=host)

    async def summarize(self, transcript: str) -> str:
        response = await self._client.chat(
            model=self._model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": transcript},
            ],
        )
        return response["message"]["content"].strip()
