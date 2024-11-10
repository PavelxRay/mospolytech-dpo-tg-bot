from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import MenuButtonCommands

from bot.handlers.commands import ALL_COMMANDS
from config import config


async def setup_bot() -> Bot:
    token = config.bot.token
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands(ALL_COMMANDS)
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

    return bot
