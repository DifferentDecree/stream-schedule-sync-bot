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
    schedule = twitch.get_schedule()

    formatter = ScheduleFormatter(Config.TIME_ZONE)
    image_file = formatter.format_image(schedule, filename="calendar.png")

    discord = DiscordClient(
        Config.DISCORD_TOKEN,
        Config.CHANNEL_ID,
        Config.MESSAGE_ID
    )
    discord.update_image(image_file, content="Weekly Stream Calendar")

if __name__ == "__main__":
    run()