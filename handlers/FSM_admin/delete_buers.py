from aiogram import Dispatcher, types

from keyboards import buttons
from config import Director
from staff_config import staff
from db.ORM import get_all_buyers, delete_buyer
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def delete_buyers(message: types.Message):
    if message.from_user.id in Director:
        buyers = await get_all_buyers()
        for buyer in buyers:
            fio = buyer['fio']
            phone = buyer['phone']
            company_name = buyer['name_of_company']
            telegramm_id = buyer['telegramm_id']

            message_text = f"Данные байера:\n" \
                        f"ФИО: {fio}\n" \
                        f"Номер телефона: {phone}\n" \
                        f"Название компании: {company_name}\n" \
                        f"ID телеграмма: {telegramm_id}"

            keyboard = InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    f"Удалить",
                    callback_data=f"delete_staff{telegramm_id}"
                )
            )

            await message.answer(message_text, reply_markup=keyboard)
        await message.answer("Это все сотрудники!", reply_markup=buttons.StartDirector)

    else:
        await message.answer("Эта команда доступна только для директора!")


async def complete_delete_buyer(call: types.CallbackQuery):
    telegramm_id = int(call.data.replace("delete_staff", "").strip())

    await delete_buyer(telegramm_id)
    await call.message.delete()

    if telegramm_id in staff:
        staff.remove(telegramm_id)
        with open('staff_config.py', 'w') as config_file:
            config_file.write(f"staff = {staff}")
        await call.message.answer(text="Байер удалён из базы данных", reply_markup=buttons.StartDirector)
    else:
        await call.message.answer(text="Ошибка: такой байер не найден в списке", reply_markup=buttons.StartDirector)




def register_delete_staff(dp: Dispatcher):
    dp.register_message_handler(delete_buyers, commands=['Все_сотрудники'])
    dp.register_callback_query_handler(complete_delete_buyer,
                                       lambda call: call.data and call.data.startswith("delete_staff"))
