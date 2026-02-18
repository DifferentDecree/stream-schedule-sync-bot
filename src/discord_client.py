import requests

class DiscordClient:
    def __init__(self, token, channel_id, message_id):
        self.token = token
        self.channel_id = channel_id
        self.message_id = message_id

    def update_message(self_ content, ping_role=False, role_id="", embed_color=5814783):
        payload = {
            "content": f"<@&{role_id}>" if ping_role and role_id else "",
            "embeds": [{
                "title": "Weekly Stream Calendar",
                "description": content,
                "color": embed_color
            }]
        }
        #Will need to review this API, likely need more in the body or URL is incorrect
        r = requests.patch(
            f"https://discord.com/api/v10/channels/{self.channel_id}/messages/{self.message_id}",
            headers={
                "Authorization": f"Bot {self.token}",
                "Content-Type": "application/json"
            },
            json=payload
        )
        r.raise_for_status()