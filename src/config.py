import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")
    MESSAGE_ID = os.getenv("MESSAGE_ID")
    ROLE_ID = os.getenv("ROLE_ID")
    PING_ROLE = os.getenv("PING_ROLE", "False") == "True"

    TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
    TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
    TWITCH_BROADCASTER_ID = os.getenv("TWITCH_BROADCASTER_ID")

    EMBED_COLOR = int(os.getenv("EMBED_COLOR", "5814783"))
    TIME_ZONE = os.getenv("TIME_ZONE", "America/New_York")