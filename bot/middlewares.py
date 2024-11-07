from typing import Any, Callable, Awaitable

from aiogram import Dispatcher
from aiogram.types import Update


async def database_session_middleware(
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any]
) -> Any:
    data["session"] = 1
    return await handler(event, data)


def setup_middlewares(dp: Dispatcher):
    dp.update.middleware.register(database_session_middleware)
