import datetime
from typing import Any, Dict

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaDocument, \
    FSInputFile
from docxtpl import DocxTemplate


documents_fsm_router = Router()


class ApplicationForm(StatesGroup):
    agreement = State()
    program_name = State()
    full_name = State()
    birth_date = State()
    registration_address = State()
    living_address = State()
    passport_number = State()
    passport_given_by = State()
    passport_given_date = State()
    SNILS = State()
    phone = State()
    email = State()


def agreement_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Продолжить", callback_data="continue")],
        [InlineKeyboardButton(text="Стоп", callback_data="stop")]
    ])
    return keyboard


@documents_fsm_router.message(Command("documents"))
async def start_filling_documents(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Начинаем заполнять данные, потребуется ввести:\n"
        "ФИО, Дату рождения, Паспортные данные, Адрес регистрации и проживания, СНИЛС, Номер телефона, Email\n"
        "\nПродолжим?",
        reply_markup=agreement_keyboard()
    )
    await state.set_state(ApplicationForm.agreement)


@documents_fsm_router.callback_query(F.data == "stop", ApplicationForm.agreement)
async def stop(call: CallbackQuery, state: FSMContext):
    await call.answer("Заполнение отменено")
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Чтобы начать заново: /documents")
    await state.clear()


def qualification_from_program(program_name: str):
    # TODO: Some logic of getting qualification name from program name
    return "Лучший специалист в мире"


def create_documents(data: Dict[str, Any], create_contract=True, create_application=False) -> list[InputMediaDocument]:
    result = []

    data["date"] = datetime.date.today()
    data["qualification_name"] = qualification_from_program(data["program_name"])

    if create_contract:
        # TODO: сделать, чтобы путь до файла брался из переменных окружения (.env)
        contract = DocxTemplate("docs_templates/contract_template.docx")
        contract.render(data)
        # TODO: сделать, чтобы папка бралась из переменных окружения (.env)
        file_path = f"created_docs/{data['full_name']} {datetime.datetime.now().strftime('%d.%m.%Y-%H.%M.%S')}.docx"
        contract.save(file_path)

        contract_to_return = InputMediaDocument(media=FSInputFile(file_path))
        result.append(contract_to_return)

    if create_application:
        # TODO: Logic of creating application
        pass

    return result


@documents_fsm_router.callback_query(F.data == "continue", ApplicationForm.agreement)
async def claim_agreement(call: CallbackQuery, state: FSMContext):
    await call.answer("Продолжаем")
    await call.message.edit_reply_markup(reply_markup=None)

    data = await state.get_data()
    if data.get("agreement"):
        await call.message.answer("Спасибо, что воспользовались ботом для записи на ДПО! Удачи в учёбе!")
        await call.message.answer_media_group(create_documents(data))
        await state.clear()
        return

    await call.message.answer("Укажите программу ДПО, на которую хотите зарегистрироваться:")
    await state.update_data(agreement=True)
    await state.set_state(ApplicationForm.program_name)


@documents_fsm_router.message(F.text, ApplicationForm.program_name)
async def capture_program_name(message: Message, state: FSMContext):
    await state.update_data(program_name=message.text)
    await message.answer("Укажите Ваше ФИО полностью:")
    await state.set_state(ApplicationForm.full_name)


@documents_fsm_router.message(F.text, ApplicationForm.full_name)
async def capture_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Теперь укажите дату рождения (ДД.ММ.ГГГГ):")
    await state.set_state(ApplicationForm.birth_date)


@documents_fsm_router.message(F.text, ApplicationForm.birth_date)
async def capture_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Заполните Ваш адрес регистрации:")
    await state.set_state(ApplicationForm.registration_address)


@documents_fsm_router.message(F.text, ApplicationForm.registration_address)
async def capture_registration_address(message: Message, state: FSMContext):
    await state.update_data(registration_address=message.text)
    await message.answer("Заполните Ваш адрес проживания:")
    await state.set_state(ApplicationForm.living_address)


@documents_fsm_router.message(F.text, ApplicationForm.living_address)
async def capture_living_address(message: Message, state: FSMContext):
    await state.update_data(living_address=message.text)
    await message.answer("Теперь укажите серию и номер паспорта:")
    await state.set_state(ApplicationForm.passport_number)


@documents_fsm_router.message(F.text, ApplicationForm.passport_number)
async def capture_passport_number(message: Message, state: FSMContext):
    await state.update_data(passport_number=message.text)
    await message.answer("Укажите, кем выдан паспорт:")
    await state.set_state(ApplicationForm.passport_given_by)


@documents_fsm_router.message(F.text, ApplicationForm.passport_given_by)
async def capture_passport_given_by(message: Message, state: FSMContext):
    await state.update_data(passport_given_by=message.text)
    await message.answer("Укажите дату выдачи паспорта (ДД.ММ.ГГГГ):")
    await state.set_state(ApplicationForm.passport_given_date)


@documents_fsm_router.message(F.text, ApplicationForm.passport_given_date)
async def capture_passport_given_date(message: Message, state: FSMContext):
    await state.update_data(passport_given_date=message.text)
    await message.answer("Теперь напишите номер СНИЛС:")
    await state.set_state(ApplicationForm.SNILS)


@documents_fsm_router.message(F.text, ApplicationForm.SNILS)
async def capture_SNILS(message: Message, state: FSMContext):
    await state.update_data(SNILS=message.text)
    await message.answer("Напишите Ваш номер телефона:")
    await state.set_state(ApplicationForm.phone)


def format_phone_number(phone_number: str):
    digits = "".join([digit for digit in phone_number if digit.isdigit()])
    formatted_number = f"+{digits[:-10]} ({digits[-10:-7]}) {digits[-7:-4]}-{digits[-4:-2]}-{digits[-2:]}"
    if formatted_number[1] == "8" and len(digits) == 11:
        formatted_number = "+7" + formatted_number[2:]
    return formatted_number


@documents_fsm_router.message(F.text, ApplicationForm.phone)
async def capture_phone(message: Message, state: FSMContext):
    await state.update_data(phone=format_phone_number(message.text))
    await message.answer("Укажите Ваш email:")
    await state.set_state(ApplicationForm.email)


@documents_fsm_router.message(F.text, ApplicationForm.email)
async def capture_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()
    await message.answer(
        f"Всё готово! Проверьте правильность внесённых данных:\n\n"
        f"Программа ДПО: {data['program_name']}\n"
        f"ФИО: {data['full_name']}\n"
        f"Дата рождения: {data['birth_date']}\n"
        f"Адрес регистрации: {data['registration_address']}\n"
        f"Адрес проживания: {data['living_address']}\n"
        f"Серия и номер паспорта: {data['passport_number']}\n"
        f"Выдан: {data['passport_given_by']}, {data['passport_given_date']}\n"
        f"СНИЛС: {data['SNILS']}\n"
        f"Номер телефона: {data['phone']}\n"
        f"Email: {data['email']}",
        reply_markup=agreement_keyboard()
    )
    await state.set_state(ApplicationForm.agreement)
