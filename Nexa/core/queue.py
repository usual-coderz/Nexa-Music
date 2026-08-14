from typing import Dict, List


class QueueManager:
    def __init__(self):
        self.queues: Dict[int, List[dict]] = {}
        self.loop: Dict[int, dict] = {}

    def add(self, chat_id: int, item: dict):
        self.queues.setdefault(chat_id, []).append(item)

    def next(self, chat_id: int):
        q = self.queues.get(chat_id, [])
        return q.pop(0) if q else None

    def clear(self, chat_id: int):
        self.queues[chat_id] = []

    def length(self, chat_id: int) -> int:
        return len(self.queues.get(chat_id, []))

    def set_loop(self, chat_id: int, enabled: bool, count: int = 0):
        self.loop[chat_id] = {"enabled": enabled, "count": count}

    def get_loop(self, chat_id: int) -> dict:
        return self.loop.get(chat_id, {"enabled": False, "count": 0})


queue = QueueManager()

CURRENT: Dict[int, dict] = {}