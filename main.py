import asyncio
from dotenv import load_dotenv

from bot.bot import setup_bot
from bot.dispatcher import setup_dispatcher
from bot.middlewares import setup_middlewares


async def main() -> None:
    load_dotenv()
    dp = setup_dispatcher()
    setup_middlewares(dp)
    bot = await setup_bot()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
