from __future__ import annotations

import re
from datetime import timedelta

import discord

from discord_summarize_bot.summarizer import Summarizer

MENTION_PATTERN = re.compile(r"<@!?\d+>")
COMMAND_PATTERN = re.compile(r"last\s+(\d+)\s+(minutes?|messages?)", re.IGNORECASE)
USAGE = "Mention me with `last N minutes` or `last N messages`, e.g. `@bot last 30 minutes`."

DISCORD_MESSAGE_LIMIT = 2000


class SummarizeBot(discord.Client):
    def __init__(
        self,
        summarizer: Summarizer,
        max_history_limit: int,
        max_lookback_minutes: int,
    ) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

        self._summarizer = summarizer
        self._max_history_limit = max_history_limit
        self._max_lookback_minutes = max_lookback_minutes

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or self.user is None or self.user not in message.mentions:
            return

        stripped = MENTION_PATTERN.sub("", message.content).strip()
        match = COMMAND_PATTERN.search(stripped)
        if match is None:
            await message.reply(USAGE)
            return

        amount = int(match.group(1))
        unit = match.group(2).lower()
        if amount <= 0:
            await message.reply(USAGE)
            return

        amount, cap_note = self._cap_amount(amount, unit)

        async with message.channel.typing():
            history = await self._fetch_history(message, amount, unit)
            transcript = self._build_transcript(history)

            if not transcript:
                await message.reply("No messages found to summarize.")
                return

            summary = await self._summarizer.summarize(transcript)

        chunks = self._chunk_message(summary)
        if cap_note:
            chunks[0] = f"{cap_note}\n{chunks[0]}"

        for chunk in chunks:
            await message.reply(chunk)

    def _cap_amount(self, amount: int, unit: str) -> tuple[int, str | None]:
        if unit.startswith("minute") and amount > self._max_lookback_minutes:
            return self._max_lookback_minutes, (
                f"-# Capped lookback to {self._max_lookback_minutes} minutes."
            )

        if unit.startswith("message") and amount > self._max_history_limit:
            return self._max_history_limit, (
                f"-# Capped to the last {self._max_history_limit} messages."
            )

        return amount, None

    async def _fetch_history(
        self, message: discord.Message, amount: int, unit: str
    ) -> list[discord.Message]:
        if unit.startswith("minute"):
            after = discord.utils.utcnow() - timedelta(minutes=amount)
            history = [
                entry
                async for entry in message.channel.history(
                    after=after, limit=self._max_history_limit, oldest_first=True
                )
            ]
        else:
            history = [
                entry
                async for entry in message.channel.history(
                    limit=amount, before=message, oldest_first=False
                )
            ]
            history.reverse()

        return [
            entry
            for entry in history
            if not entry.author.bot and entry.id != message.id
        ]

    @staticmethod
    def _build_transcript(history: list[discord.Message]) -> str:
        lines = [
            f"{entry.author.display_name}: {entry.clean_content}"
            for entry in history
            if entry.clean_content
        ]

        return "\n".join(lines)

    @staticmethod
    def _chunk_message(text: str, limit: int = DISCORD_MESSAGE_LIMIT) -> list[str]:
        chunks: list[str] = []
        current = ""
        for line in text.splitlines(keepends=True):
            if len(current) + len(line) > limit:
                chunks.append(current)
                current = ""

            current += line

        if current:
            chunks.append(current)

        return chunks
