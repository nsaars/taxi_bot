from abc import ABC
from typing import Any, Callable, Dict, Awaitable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.fsm.storage.base import BaseStorage, StorageKey
from aiogram.types import TelegramObject

from states.fsm_context import CustomFSMContext


class CustomFSMContextMiddleware(BaseMiddleware, ABC):
    def __init__(self, storage: BaseStorage):
        self.storage = storage
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        bot = data['bot']
        chat = data['event_chat']
        user = data['event_from_user']

        if chat and user:
            key = StorageKey(bot_id=bot.id, user_id=user.id, chat_id=chat.id)
            name = user.first_name or '' + user.last_name or ''
            data['state'] = CustomFSMContext(storage=self.storage, key=key, username=user.username, name=name)
        return await handler(event, data)
