from config import Config
from twitch import TwitchClient
from formatter import ScheduleFormatter
from discord_client import DiscordClient

def run():
    twitch = TwitchClient(
        Config.TWITCH_CLIENT_ID,
        Config.TWITCH_CLIENT_SECRET,
        Config.TWITCH_BROADCASTER_ID
    )

    discord = DiscordClient(
        Config.DISCORD_TOKEN,
        Config.CHANNEL_ID,
        Config.MESSAGE_ID
    )
    formatter = ScheduleFormatter(Config.TIME_ZONE)

    schedule = twitch. get_schedule()
    formatted = formatter.format_horizontal_grid(schedule)

    discord.update_message(
        formatted,
        ping_role=Config.PING_ROLE,
        role_id=Config.ROLE_ID,
        embed_color=Config.EMBED_COLOR
    )

if __name__ == "__main__":
    run()