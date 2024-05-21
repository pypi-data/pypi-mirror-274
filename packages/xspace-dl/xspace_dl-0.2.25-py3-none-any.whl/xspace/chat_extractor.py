import requests
import json
import logging
import os
from urllib.parse import urlparse

class ChatExtractor:
    def __init__(self, chat_token: str, endpoint: str):
        self.chat_token = chat_token
        self.endpoint = endpoint
        self.logger = logging.getLogger(__name__)
    
    def extract(self):
        self.logger.info(f"Extracting chat from endpoint: {self.endpoint}")
        response = requests.post(
            f"{self.endpoint}/api/v2/accessChat",
            json={"chat_token": self.chat_token}
        )
        response.raise_for_status()
        chat_data = response.json()
        chat_file = f"chat_{self.chat_token}.json"
        with open(chat_file, "w", encoding="utf-8") as file:
            json.dump(chat_data, file, indent=4)
        self.logger.info(f"Chat data saved to {chat_file}")

