from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import buttons
from config import Director, bot, Admins
from staff_config import staff

from db.ORM import insert_bayers, check_telegramm_id_existence


class RegistrationStates(StatesGroup):
    full_name = State()
    phone_number = State()
    company_name = State()
    submit = State()
    process_receipt = State()
    send_admin = State()
    submit_admin = State()


async def cmd_start(message: types.Message):
    telegramm_id = str(message.from_user.id)

    if telegramm_id in Director:
        await message.answer("Админы и Директора не могут стать байерами")
    elif telegramm_id in Admins:
        await message.answer("Админы и Директора не могут стать байерами")
    else:
        is_registered = await check_telegramm_id_existence(int(telegramm_id))  # Преобразование в целое число

        if is_registered:
            await message.answer("Данный телеграмм аккаунт уже зарегистрирован.")
        else:
            await message.answer("Привет! Для регистрации введите своё ФИО:", reply_markup=buttons.cancel_markup)
            await RegistrationStates.full_name.set()


async def load_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        global full_name
        full_name = message.text
        data['fio'] = full_name
    await message.answer("Отлично! Теперь введите свой номер телефона:")
    await RegistrationStates.next()


async def load_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        global phone_number
        phone_number = message.text
        data['phone'] = phone_number
    await message.answer("Отлично! Теперь введите название своей компании:")
    await RegistrationStates.next()


async def load_company_name(message: types.Message, state: FSMContext):
    global user_id
    global company_name
    user_id = int(message.from_user.id)
    company_name = message.text

    async with state.proxy() as data:
        data['name_of_company'] = company_name
        data['telegram_id'] = user_id

    await message.answer(f"Данные регистрации!\n\n"
                         f"Ваши данные:\n"
                         f"ФИО: {full_name}\n"
                         f"Номер телефона: {phone_number}\n"
                         f"Название компании: {company_name}")
    await message.answer("Верно ?", reply_markup=buttons.submit_markup)
    await RegistrationStates.next()


async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        async with state.proxy() as data:
            await send_admin_data(data)
        await message.answer(text="Отправлено на проверку администратору! ✅\n"
                                  "Подождите немного ⏳", reply_markup=buttons.StartClient)

        await state.finish()
    elif message.text.lower() == 'нет':
        await message.answer("Отменено!", reply_markup=buttons.StartClient)
        await state.finish()


async def send_admin_data(data):
    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    button_yes = InlineKeyboardButton("Да✅", callback_data="button_yes")
    button_no = InlineKeyboardButton("Нет❌", callback_data="button_no")
    inline_keyboard.add(button_yes, button_no)

    caption = (f"Поступил запрос от пользователя с ID {user_id} на байерство\n\n"
               f"Данные байера:\n"
               f"ФИО: {full_name}\n"
               f"Номер телефона: {phone_number}\n"
               f"Название компании: {company_name}")

    for admin in Director:
        await bot.send_message(chat_id=admin, text=caption, reply_markup=inline_keyboard)


async def answer_yes(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(user_id,
                           text="Регистрация прошла успешно! ✅",
                           reply_markup=buttons.StartStaff)
    for i in Director:
        await bot.send_message(i, text='Подтверждено! ✅')
        await insert_bayers(company_name, phone_number, full_name, int(user_id))  # Преобразуйте user_id в int
        staff.append(user_id)
        with open('staff_config.py', 'w') as config_file:
            config_file.write(f"staff = {staff}")
        await state.finish()


async def answer_no(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(user_id,
                           text="Вам отказано! ❌",
                           reply_markup=buttons.StartClient)
    for i in Director:
        await bot.send_message(i, text='Отклонено! ❌')
        await state.finish()


async def cancel_reg(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Отменено!', reply_markup=None)


def registration(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(cmd_start, commands=['become_buyer'], commands_prefix='_/')
    dp.register_message_handler(load_fullname, state=RegistrationStates.full_name)
    dp.register_message_handler(load_phone_number, state=RegistrationStates.phone_number)
    dp.register_message_handler(load_company_name, state=RegistrationStates.company_name)
    dp.register_message_handler(submit, state=RegistrationStates.submit)
    dp.register_callback_query_handler(answer_yes, lambda c: c.data == "button_yes")
    dp.register_callback_query_handler(answer_no, lambda c: c.data == "button_no")
