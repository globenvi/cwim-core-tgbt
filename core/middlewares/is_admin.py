import json

from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message


class isAdmin(BaseFilter):
    def __init__(self) -> None:
        # Assuming config.json is in the same directory as your script
        with open('config.json', 'r') as f:
            config = json.load(f)
        self.user_ids = config['admins']
        print(f"Admin IDs: {self.user_ids}")

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.user_ids, int):
            return message.from_user.id == self.user_ids
        return message.from_user.id in self.user_ids