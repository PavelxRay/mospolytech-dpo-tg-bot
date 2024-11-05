from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

commands_router = Router()


@commands_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Выберите, что вам интересно узнать о программах дополнительного профессионального образования (ДПО):\n\n"
        "<b>🔹 Просмотр доступных программ</b>\n"
        "Узнайте о курсах и выберите подходящий для себя.\n\n"
        "<b>🔹 Рекомендации по выбору программы</b>\n"
        "Получите помощь в подборе курсов, которые будут полезны именно вам.\n\n"
        "<b>🔹 Заполнение заявления и договора</b>\n"
        "Заполните и получите готовые документы на обучение в формате Word."
    )


@commands_router.message(Command("programs", "advice"))
async def command_handler(message: Message) -> None:
    await message.answer("Пока не реализовано")
