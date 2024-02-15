from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Director, bot

user_id = None
username = None
fullname = None


class RegistrationStates(StatesGroup):
    full_name = State()
    phone_number = State()
    company_name = State()
    submit = State()
    process_receipt = State()
    send_admin = State()
    submit_admin = State()


async def cmd_start(message: types.Message):
    await message.answer("Привет! Для регистрации введите свое ФИО:", reply_markup=buttons.cancel_markup)
    await RegistrationStates.full_name.set()


async def load_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['full_name'] = message.text
    await message.answer("Отлично! Теперь введите свой номер телефона:")
    await RegistrationStates.next()


async def load_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await message.answer("Отлично! Теперь введите название своей компании:")
    await RegistrationStates.next()


async def load_company(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['company_name'] = message.text

    await message.answer(f"Данные регистрации!\n\n"
                         f"Ваши данные:\n"
                         f"ФИО: {data['full_name']}\n"
                         f"Номер телефона: {data['phone_number']}\n"
                         f"Название компании: {data['company_name']}")
    await message.answer("Верно ?")
    await RegistrationStates.next()


async def submit(message: types.Message, state: FSMContext):
    if message.text == 'да':
        global user_id
        global fullname
        global username

        async with state.proxy() as data:
            user_id = message.chat.id
            fullname = message.chat.full_name
            username = message.chat.username

            await send_admin_data(data, state)

            # Запись в базу

            await message.answer("Отправлено на проверку администратору! ⏳", reply_markup=buttons.StartClient)
            await state.finish()
    elif message.text == 'нет':
        await message.answer("Отменено!")
        await state.finish()


async def send_admin_data(data, state: FSMContext):
    global fullname
    global user_id
    global username

    if not username:
        username = fullname

    async with state.proxy() as data:
        data["user_id"] = user_id
        data["user_name"] = f"@{username}"

    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    button_yes = InlineKeyboardButton("Да✅", callback_data="button_yes")
    button_no = InlineKeyboardButton("Нет❌", callback_data="button_no")
    inline_keyboard.add(button_yes, button_no)

    caption = (f"Поступил запрос от пользователя с ID {user_id} на байерство\n\n"
               f"Ваши данные:\n"
               f"ФИО: {data['full_name']}\n"
               f"Номер телефона: {data['phone_number']}\n"
               f"Название компании: {data['company_name']}")

    for Admin in Director:
        await bot.send_message(
            chat_id=Admin,
            text=caption, reply_markup=inline_keyboard)


async def answer_yes(message: types.Message, state: FSMContext):
    global user_id
    await bot.send_message(user_id, text="Регистрация прошла успешно! ✅",
                           reply_markup=buttons.StartStaff)

    for Admin in Director:
        await bot.send_message(chat_id=Admin, text='Подтверждено! ✅')


async def answer_no(message: types.Message):
    global user_id
    await bot.send_message(user_id,
                           text="Вам отказано! ❌", reply_markup=buttons.StartClient)
    for Admin in Director:
        await bot.send_message(chat_id=Admin, text='Отклонено! ❌')


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=None)


def registration(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(cmd_start, commands=['become_buyer'], commands_prefix='_/')
    dp.register_message_handler(load_fullname, state=RegistrationStates.full_name)
    dp.register_message_handler(load_phone_number, state=RegistrationStates.phone_number)
    dp.register_message_handler(submit, state=RegistrationStates.submit)

    dp.register_message_handler(send_admin_data, state=RegistrationStates.send_admin)

    dp.register_callback_query_handler(answer_yes, lambda call: call.data == "button_yes")
    dp.register_callback_query_handler(answer_no, lambda call: call.data == "button_no")
