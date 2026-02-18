# Stream Schedule Sync Bot

Syncronizes your Twitch stream schedule to a **custom Discord calendar** embed automatically using GitHub Actions.

**Author:** DifferentDecree

---

## Features
 
- Horizontal weekly calendar (monospaced grid)
- Strikethrough canceled streams
- Role ping toggle
- Configurable embed color and timezone
- Fully open-source and future-proof
- GitHub Actions cron automation

---

## Setup

### Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Copy the bot token from "Bot" section -> `DISCORD_TOKEN`
4. Invite the bot to your server with:
    - Scopes: `bot`
    - Permissions: `Send Messages`, `Embed Links`, `Read Message History`

---

### Create a Channel & Message

1. Optional: Create a dedicated channel for your calendar (e.g., `#calendar`)
2. Send a blank message -> copy its ID -> `MESSAGE_ID`
3. Copy the channel ID -> `CHANNEL_ID`

---

### GitHub Actions Secrets

Fork this repo -> Go to your repo -> **Settings -> Secrets -> Actions -> New repository secret**:

- `DISCORD_TOKEN`
- `CHANNEL_ID`
- `MESSAGE_ID`
- `ROLE_ID` (optional)
- `PING_ROLE`
- `TWITCH_CLIENT_ID`
- `TWITCH_CLIENT_SECRET`
- `TWITCH_BROADCASTER_ID`
- `EMBED_COLOR`
- `TIMEZONE`

> Make sure your secrets match the keys in `.env.example`

---

### Run Locally (Optional)

```bash
python src/main.py