from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    discord_token: str
    ollama_model: str
    ollama_host: str
    max_history_limit: int
    max_lookback_minutes: int

    @classmethod
    def from_env(cls) -> Config:
        token = os.environ.get("DISCORD_TOKEN")
        if not token:
            raise RuntimeError("DISCORD_TOKEN environment variable is required")

        return cls(
            discord_token=token,
            ollama_model=os.environ.get("OLLAMA_MODEL", "gemma4:26b"),
            ollama_host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
            max_history_limit=int(os.environ.get("MAX_HISTORY_LIMIT", "500")),
            max_lookback_minutes=int(
                os.environ.get("MAX_LOOKBACK_MINUTES", str(60 * 24 * 30))
            ),
        )
