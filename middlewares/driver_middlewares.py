from abc import ABC
from datetime import datetime
from typing import Any, Callable, Dict, Awaitable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.fsm.storage.base import BaseStorage
from aiogram.types import TelegramObject

from data.config import ADMIN
from functions.driver_crud import update_driver, get_driver_by_id
from utils.scores import ScoreCounter


class DriverMiddleware(BaseMiddleware, ABC):
    MIN_TIME_DELTA = 60

    def __init__(self, storage: BaseStorage):
        self.storage = storage
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        try:
            storage_data = self.storage.__dict__.get('storage', None)

            if storage_data:
                state_data = list(storage_data.values())[0].data
            else:
                raise AttributeError("Storage attribute not found or has unexpected structure")
        except AttributeError as e:
            print(f"Error accessing storage data: {e}")
            state_data = None

        if state_data:
            current_driver = state_data.get('current_driver')
            if current_driver and event.from_user.id != ADMIN:
                if get_driver_by_id(current_driver['id']).get('is_blocked'):
                    return
                now = datetime.now()
                scores_updated_at = datetime.strptime(current_driver['scores_updated_at'], "%Y-%m-%dT%H:%M:%S")

                time_delta = now - scores_updated_at
                if time_delta.seconds > self.MIN_TIME_DELTA:
                    driver = get_driver_by_id(current_driver['id'])
                    new_scores = ScoreCounter.get_driver_new_scores(driver)
                    update_driver(driver['id'], {'scores': driver['scores'] + new_scores,
                                                 'scores_updated_at': now.strftime("%Y-%m-%dT%H:%M:%S")})
                    await data['state'].update_data({'current_driver': driver})

        return await handler(event, data)
