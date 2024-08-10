import json
import requests

class SlackNotifier:
    def __init__(self, webhook_url, username="Q&A-Bot", icon_emoji=":robot_face:"):
        self.webhook_url = webhook_url
        self.username = username
        self.icon_emoji = icon_emoji

    def send_message(self, message):
        data = {
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "text": "Here are the answers:",
            "attachments": [
                {
                    "color": "#36a64f",
                    "type": "mrkdwn",
                    "text": json.dumps(message, indent=4) if isinstance(message, dict) else message
                }
            ]
        }

        response = requests.post(
            self.webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")


