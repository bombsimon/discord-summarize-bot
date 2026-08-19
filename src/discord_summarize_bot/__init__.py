from dotenv import load_dotenv

from discord_summarize_bot.bot import SummarizeBot
from discord_summarize_bot.config import Config
from discord_summarize_bot.summarizer import (
    GeminiSummarizer,
    OllamaSummarizer,
    Summarizer,
)


def _build_summarizer(config: Config) -> Summarizer:
    if config.summary_provider == "gemini":
        assert config.gemini_api_key is not None
        return GeminiSummarizer(
            model=config.gemini_model, api_key=config.gemini_api_key
        )

    return OllamaSummarizer(model=config.ollama_model, host=config.ollama_host)


def main() -> None:
    load_dotenv()
    config = Config.from_env()

    bot = SummarizeBot(
        summarizer=_build_summarizer(config),
        max_history_limit=config.max_history_limit,
        max_lookback_minutes=config.max_lookback_minutes,
    )

    bot.run(config.discord_token)
