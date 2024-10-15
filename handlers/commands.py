from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

commands_router = Router()


@commands_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Привет! Здесь Вы можете:\n"
        "Узнать о доступных программах ДПО\n(команда /programs)\n\n"
        "Получить рекомендацию по выбору подходящей программы ДПО\n(команда /advice)\n\n"
        "Заполнить заявление и договор на обучение и получить готовый Word-файл\n(команда /documents)"
    )


@commands_router.message(Command("programs", "advice"))
async def command_handler(message: Message) -> None:
    await message.answer("Пока не реализовано")
