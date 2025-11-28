import slack
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

SLACK_TOKEN = os.getenv('SLACK_TOKEN')

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        print("Initializing Notification Manager....")
        self.client = slack.WebClient(token=SLACK_TOKEN)

    def send_notification(self, message):
        print(f"Sending Notification ... {message}")
        self.client.chat_postMessage(channel="#test", text=message)