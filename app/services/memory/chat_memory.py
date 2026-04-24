import json
from app.services.memory.redis_client import RedisClient


class ChatMemory:

    def __init__(self):
        self.redis = RedisClient()

    def get_history(self, session_id: str):

        data = self.redis.get(session_id)

        if not data:
            return []

        return json.loads(data)

    def add_message(self, session_id: str, message: str):

        history = self.get_history(session_id)
        history.append(message)

        self.redis.set(session_id, json.dumps(history))
