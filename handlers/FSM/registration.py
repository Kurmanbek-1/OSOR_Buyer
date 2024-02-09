import json
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Director
import buttons
from aiogram.dispatcher.filters import Text


class RegistrationStates(StatesGroup):
    full_name = State()
    phone_number = State()
    company_name = State()


# Загружаем данные из файла при запуске бота
try:
    with open('reg.json', 'r') as file:
        registered_users = json.load(file)
except FileNotFoundError:
    registered_users = {}


async def cmd_start(message: types.Message):
    await message.answer("Привет! Для регистрации введите свое ФИО:", reply_markup=buttons.cancel_markup)
    await RegistrationStates.full_name.set()


async def load_fullname(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await message.answer("Отлично! Теперь введите свой номер телефона:")
    await RegistrationStates.next()


async def load_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    await message.answer("Отлично! Теперь введите название своей компании:")
    await RegistrationStates.next()


async def load_company_name(message: types.Message, state: FSMContext):
    company_name = message.text
    await state.update_data(company_name=company_name)
    user_data = await state.get_data()
    await state.finish()

    # Вывод данных
    output_message = f"Спасибо за регистрацию!\n\n" \
                     f"Ваши данные:\n" \
                     f"ФИО: {user_data['full_name']}\n" \
                     f"Номер телефона: {user_data['phone_number']}\n" \
                     f"Название компании: {user_data['company_name']}"

    await message.answer(output_message)

    # Добавление ID в файл config.py
    with open('config.py', 'r') as config_file:
        config_content = config_file.read()

    with open('config.py', 'a') as config_file:
        config_file.write(f"\nstaff.append({message.from_user.id})\n")

    # Сохранение данных в файл
    with open('reg.json', 'w') as file:
        json.dump(registered_users, file)


async def cmd_get_registered_users(message: types.Message):
    if message.from_user.id in Director:
        if registered_users:
            for user_id, user_data in registered_users.items():
                # Вывод данных
                output_message = (f"Сотрудник/Байер 🧑🏻‍💼👨🏼‍💼"
                                  f"\n---------------------------------\n"
                                  f"ID-телеграма: {user_id}\n"
                                  f"ФИО: {user_data['full_name']}\n"
                                  f"Номер телефона: {user_data['phone_number']}\n"
                                  f"Название компании: {user_data['company_name']}"
                                  f"\n---------------------------------\n")

                # Создаем кнопку удаления
                inline_btn = InlineKeyboardButton('Удалить', callback_data=f'remove_user_{user_id}')
                inline_kb = InlineKeyboardMarkup().add(inline_btn)

                await message.answer(output_message, reply_markup=inline_kb)
        else:
            await message.answer("Пока нет зарегистрированных пользователей.")
    else:
        await message.answer("У вас нет доступа к этой команде.")


async def cmd_remove_user_callback(query: types.CallbackQuery):
    user_id_to_remove = int(query.data.split('_')[-1])
    removed_user_data = registered_users.pop(user_id_to_remove, None)
    if removed_user_data:
        output_message = (f"Пользователь удален из списка. ❌"
                          f"\n---------------------------------\n")
        output_message += f"ФИО: {removed_user_data['full_name']}\n"
        output_message += f"Номер телефона: {removed_user_data['phone_number']}\n"
        output_message += (f"Название компании: {removed_user_data['company_name']}"
                           f"\n---------------------------------")
        await query.message.edit_text(output_message)

    else:
        await query.message.edit_text(f"Пользователь с ID {user_id_to_remove} не найден в списке.")

    with open('reg.json', 'w') as file:
        json.dump(registered_users, file)


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=None)


def registration(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(cmd_start, commands=['зарегестрироваться_на_байерство_'], commands_prefix='_/')
    dp.register_message_handler(load_fullname, state=RegistrationStates.full_name)
    dp.register_message_handler(load_phone_number, state=RegistrationStates.phone_number)
    dp.register_message_handler(load_company_name, state=RegistrationStates.company_name)

    # Добавляем новые команды
    dp.register_message_handler(cmd_get_registered_users, commands=['Зарегестрированные'])
    dp.register_callback_query_handler(cmd_remove_user_callback, text_contains='remove_user')
