from typing import Any, Callable, Awaitable

from aiogram import Dispatcher
from aiogram.types import Update

from database.database import database


async def database_session_middleware(
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any]
) -> Any:
    async with database.session() as session:
        data["session"] = session
        result = await handler(event, data)
        await session.commit()


def setup_middlewares(dp: Dispatcher):
    dp.update.middleware.register(database_session_middleware)
