import asyncio

from bot.bot import setup_bot
from bot.dispatcher import setup_dispatcher
from bot.middlewares import setup_middlewares
from database.database import setup_database


async def main() -> None:
    dp = setup_dispatcher()
    setup_middlewares(dp)
    setup_database(dp)
    bot = await setup_bot()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
