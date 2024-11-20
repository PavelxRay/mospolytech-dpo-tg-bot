from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from bot.handlers.faq import FAQ_DATA


def agreement_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Продолжить", callback_data="continue")],
        [InlineKeyboardButton(text="Стоп", callback_data="stop")]
    ])
    return keyboard


def after_start_keyboard():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="📄 Заявление и договор")],
            [KeyboardButton(text="📋 Просмотр программ")],
            [KeyboardButton(text="📊 Рекомендации")],
            [KeyboardButton(text="❓ FAQ")],
        ])
    return keyboard


def generate_faq_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    for question in FAQ_DATA.keys():
        keyboard.add(InlineKeyboardButton(text=question, callback_data=f"faq:{question}"))
    keyboard.add(InlineKeyboardButton(text="❌ Отмена", callback_data="faq:cancel"))
    return keyboard