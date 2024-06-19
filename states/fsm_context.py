from json import loads

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage, StorageKey
from typing import Dict, Any, Optional

from functions.state_crud import update_state, create_state, get_state_by_user_telegram_id, get_state_by_user_id
from functions.user_crud import get_user_by_telegram_id, get_all_users, create_user


class CustomFSMContext(FSMContext):
    def __init__(self, storage: BaseStorage, key: StorageKey, username, name) -> None:
        super().__init__(storage, key)
        self.state = get_state_by_user_telegram_id(int(self.key.user_id))
        if not self.state:
            user = get_user_by_telegram_id(self.key.user_id)
            print(user, 1)
            if not user:
                user = create_user({'telegram_id': self.key.user_id, 'telegram_username': username, 'telegram_name': name})
            print(2, user, 3)
            self.state = create_state({'user_id': user['id']})

    async def set_state(self, state: str = None) -> None:
        await super().set_state(state)
        update_state(self.state['id'], {'title': state})

    async def set_data(self, data: Dict[str, Any]) -> None:
        await super().set_data(data)
        update_state(self.state['id'], {'data': data})

    async def update_data(self, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Dict[str, Any]:
        updated_data = await super().update_data(data, **kwargs)
        update_state(self.state['id'], {'data': updated_data})
        return updated_data

    async def clear(self) -> None:
        await super().clear()
        update_state(self.state['id'], {'title': None, 'data': {}})

    @staticmethod
    async def set_all_states(bot, storage):
        users = get_all_users()

        for user in users:
            state = get_state_by_user_id(user['id'])
            if state:
                user_storage_key = StorageKey(bot.id, user['telegram_id'], user['telegram_id'])
                user_context = FSMContext(storage=storage, key=user_storage_key)
                await user_context.set_state(state['title'])
                if state.get('data'):
                    await user_context.set_data(state.get('data'))
