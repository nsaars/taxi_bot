import asyncio

import orjson
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import handlers
from data import config
from middlewares.driver_middlewares import DriverMiddleware
from middlewares.state_middlewares import CustomFSMContextMiddleware
from states.fsm_context import CustomFSMContext


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(handlers.crud_handlers.prepare_router())
    dp.include_router(handlers.menu_handlers.prepare_router())


def setup_middlewares(dp: Dispatcher) -> None:
    dp.message.middleware(CustomFSMContextMiddleware(storage=dp.storage))
    dp.callback_query.middleware(CustomFSMContextMiddleware(storage=dp.storage))
    dp.message.middleware(DriverMiddleware(storage=dp.storage))
    dp.callback_query.middleware(DriverMiddleware(storage=dp.storage))


async def setup_aiogram(dp: Dispatcher) -> None:
    setup_handlers(dp)
    setup_middlewares(dp)


async def aiogram_on_startup_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    await setup_aiogram(dispatcher)
    await CustomFSMContext.set_all_states(bot, dispatcher.storage)


async def aiogram_on_shutdown_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    await bot.session.close()
    await dispatcher.storage.close()


def main() -> None:
    session = AiohttpSession(
        json_loads=orjson.loads,
    )

    bot = Bot(
        token=config.BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    storage = MemoryStorage()

    dp = Dispatcher(
        storage=storage,
    )
    dp.startup.register(aiogram_on_startup_polling)
    dp.shutdown.register(aiogram_on_shutdown_polling)
    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    main()
