import requests

class DiscordClient:
    def __init__(self, token, channel_id, message_id):
        self.token = token
        self.channel_id = channel_id
        self.message_id = message_id

    def update_image(self, image_path, content=""):
        """Update the existing message with a new image."""
        if not self.message_id:
            raise ValueError("MESSAGE_ID must be set to update a message.")

        with open(image_path, "rb") as f:
            r = requests.patch(
                f"https://discord.com/api/v10/channels/{self.channel_id}/messages/{self.message_id}",
                headers={"Authorization": f"Bot {self.token}"},
                files={"file": f},
                data={"content": content}
            )
        r.raise_for_status()
        return r.json()