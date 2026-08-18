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

3. Make sure Ollama is running locally and has the model pulled, e.g.:

   ```sh
   ollama pull gemma4:26b
   ```

4. Create a `.env` file in the project root:

   ```sh
   DISCORD_TOKEN=your-bot-token
   OLLAMA_MODEL=gemma4:26b             # optional, defaults to gemma4:26b
   OLLAMA_HOST=http://localhost:11434  # optional
   MAX_HISTORY_LIMIT=500               # optional, caps how many messages are fetched
   MAX_LOOKBACK_MINUTES=43200          # optional, caps "last N minutes" (default 30 days)
   ```

5. Run the bot:

   ```sh
   uv run discord-summarize-bot
   ```
