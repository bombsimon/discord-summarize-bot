# discord-summarize-bot

A Discord bot that summarizes recent channel activity on demand, using a
local [Ollama](https://ollama.com) model.

Mention the bot with one of:

```sh
@bot last 30 minutes
@bot last 50 messages
```

> [!TIP]
> Name your bot "Summarize" so mentions read naturally, e.g.
> `@Summarize last 10 messages`.

It fetches the matching message history, sends it to your local Ollama
model, and replies with a short, dense TL;DR in bullet points.

## Setup

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Create a Discord application and bot user at the
   [Discord Developer Portal](https://discord.com/developers/applications),
   then:
   - Under **Bot**, enable the **Message Content Intent**.
   - Copy the bot token.
   - Under **OAuth2 → URL Generator**, select the `bot` scope and the
     `Send Messages` / `Read Message History` permissions, then use the
     generated URL to invite the bot to your server.

3. Choose a summary provider:

   - **Ollama** (default) - runs a model locally. Make sure Ollama is
     running and has the model pulled, e.g.:

     ```sh
     ollama pull gemma3:27b
     ```

   - **Gemini** - calls the Gemini API instead, no local model needed.
     Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).

4. Create a `.env` file in the project root:

   ```sh
   DISCORD_TOKEN=your-bot-token
   SUMMARY_PROVIDER=ollama              # optional, "ollama" (default) or "gemini"

   # Used when SUMMARY_PROVIDER=ollama
   OLLAMA_MODEL=gemma3:27b              # optional, defaults to gemma3:27b
   OLLAMA_HOST=http://localhost:11434   # optional

   # Used when SUMMARY_PROVIDER=gemini
   GEMINI_API_KEY=your-gemini-api-key   # required when SUMMARY_PROVIDER=gemini
   GEMINI_MODEL=gemini-3.5-flash-lite   # optional, defaults to gemini-3.5-flash-lite

   MAX_HISTORY_LIMIT=500                # optional, caps how many messages are fetched
   MAX_LOOKBACK_MINUTES=43200           # optional, caps "last N minutes" (default 30 days)
   ```

5. Run the bot:

   ```sh
   uv run discord-summarize-bot
   ```
