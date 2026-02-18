import requests

class TwitchClient:
    def __init__(self, client_id, client_secret, broadcaster_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.broadcaster_id = broadcaster_id
        self.token = self._get_token()

    def _get_token(self):
        r = requests.post(
            "https://id.twitch.tv/oauth2/token",
            params={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials"
            }
        )
        r.raise_for_status()
        return r.json()["access_token"]

    def get_schedule(self):
        r = requests.get(
            f"https://api.twitch.tv/helix/schedule?broadcaster_id={self.broadcaster_id}",
            headers={
                "Client-ID": self.client_id,
                "Authorization": f"Bearer {self.token}"
            }
        )
        r.raise_for_status()
        print (r.json())
        return r.json()