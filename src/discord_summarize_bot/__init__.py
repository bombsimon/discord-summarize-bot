from dotenv import load_dotenv

from discord_summarize_bot.bot import SummarizeBot
from discord_summarize_bot.config import Config
from discord_summarize_bot.summarizer import Summarizer


def main() -> None:
    load_dotenv()
    config = Config.from_env()

    summarizer = Summarizer(
        model=config.ollama_model,
        host=config.ollama_host,
    )

    bot = SummarizeBot(
        summarizer=summarizer,
        max_history_limit=config.max_history_limit,
        max_lookback_minutes=config.max_lookback_minutes,
    )

    bot.run(config.discord_token)
