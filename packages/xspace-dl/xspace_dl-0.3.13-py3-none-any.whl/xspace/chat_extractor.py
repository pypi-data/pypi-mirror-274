import requests
import json
import logging

class ChatExtractor:
    def __init__(self, cookies_file, output_path):
        self.spaces_id = ""
        self.media_key = ""
        self.access_token = ""
        self.chat_token = ""
        self.cookies = self.load_cookies(cookies_file)
        self.csrf_token = self.cookies['ct0']
        self.auth_token = self.cookies['auth_token']
        self.bearer_token = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        self.output_path = output_path

    def load_cookies(self, path):
        cookies = {}
        with open(path, 'r') as f:
            for line in f:
                if not line.startswith(("#", "\n")):
                    parts = line.strip().split('\t')
                    cookies[parts[5]] = parts[6]
        return cookies

    def set_media_key(self):
        data = {
            'variables': {
                "id": self.spaces_id,
                "isMetatagsQuery": False,
                "withSuperFollowsUserFields": True,
                "withUserResults": True,
                "withBirdwatchPivots": False,
                "withReactionsMetadata": False,
                "withReactionsPerspective": False,
                "withSuperFollowsTweetFields": True,
                "withReplays": True,
                "withScheduledSpaces": True
            }
        }
        response = requests.get(
            'https://x.com/i/api/graphql/jyQ0_DEMZHeoluCgHJ-U5Q/AudioSpaceById',
            headers={
                "x-csrf-token": self.csrf_token,
                "Authorization": self.bearer_token,
                "Cookie": '; '.join([f"{key}={value}" for key, value in self.cookies.items()]),
                'Content-Type': 'application/json'
            },
            json=data
        )
        response.raise_for_status()
        self.media_key = response.json()['data']['audioSpace']['metadata']['media_key']
        logging.info(f"Media key set: {self.media_key}")

    def set_chat_token(self):
        response = requests.get(
            f'https://x.com/i/api/1.1/live_video_stream/status/{self.media_key}?client=web&use_syndication_guest_id=false&cookie_set_host=x.com',
            headers={
                "x-csrf-token": self.csrf_token,
                "Authorization": self.bearer_token,
                "Cookie": '; '.join([f"{key}={value}" for key, value in self.cookies.items()])
            }
        )
        response.raise_for_status()
        self.chat_token = response.json()['chatToken']
        logging.info(f"Chat token set: {self.chat_token}")

    def set_access_token(self):
        response = requests.post(
            'https://proxsee.pscp.tv/api/v2/accessChatPublic',
            json={"chat_token": self.chat_token}
        )
        response.raise_for_status()
        self.access_token = response.json()['access_token']
        logging.info(f"Access token set: {self.access_token}")

    def get_current_caption(self, cursor):
        response = requests.post(
            'https://chatman-replay-eu-central-1.pscp.tv/chatapi/v1/history',
            json={"access_token": self.access_token, "cursor": cursor, "limit": 1000, "since": None, "quick_get": True}
        )
        response.raise_for_status()
        return response.json()

    def get_caption(self, spaces_id):
        logging.info(f"Starting caption extraction for space ID: {spaces_id}")
        self.spaces_id = spaces_id
        self.set_media_key()
        self.set_chat_token()
        self.set_access_token()
        cursor_exist = True
        cursor = ""
        with open(self.output_path, 'w', encoding='utf-8') as f:
            while cursor_exist:
                raw_data = self.get_current_caption(cursor)
                for message in raw_data['messages']:
                    payload = json.loads(message['payload'])
                    body = json.loads(payload['body'])
                    if "final" in body and body['final']:
                        f.write(f"{body['programDateTime']} {body['username']}:  {body['body']}\n")
                cursor = raw_data.get('cursor')
                cursor_exist = bool(cursor and int(cursor) > 0)
        logging.info(f"Finished extracting captions to {self.output_path}")
