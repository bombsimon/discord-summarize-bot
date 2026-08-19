from __future__ import annotations

import os
from dataclasses import dataclass

VALID_SUMMARY_PROVIDERS = ("ollama", "gemini")


@dataclass(frozen=True)
class Config:
    discord_token: str
    summary_provider: str
    ollama_model: str
    ollama_host: str
    gemini_model: str
    gemini_api_key: str | None
    max_history_limit: int
    max_lookback_minutes: int

    @classmethod
    def from_env(cls) -> Config:
        token = os.environ.get("DISCORD_TOKEN")
        if not token:
            raise RuntimeError("DISCORD_TOKEN environment variable is required")

        summary_provider = os.environ.get("SUMMARY_PROVIDER", "ollama").lower()
        if summary_provider not in VALID_SUMMARY_PROVIDERS:
            raise RuntimeError(
                f"SUMMARY_PROVIDER must be one of {VALID_SUMMARY_PROVIDERS}"
            )

        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        if summary_provider == "gemini" and not gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is required when "
                "SUMMARY_PROVIDER=gemini"
            )

        return cls(
            discord_token=token,
            summary_provider=summary_provider,
            ollama_model=os.environ.get("OLLAMA_MODEL", "gemma3:27b"),
            ollama_host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
            gemini_model=os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite"),
            gemini_api_key=gemini_api_key,
            max_history_limit=int(os.environ.get("MAX_HISTORY_LIMIT", "500")),
            max_lookback_minutes=int(
                os.environ.get("MAX_LOOKBACK_MINUTES", str(60 * 24 * 30))
            ),
        )
