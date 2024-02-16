from aiogram import Dispatcher, types
from config import Director
from staff_config import staff
import buttons
from db.ORM import get_all_buyers, delete_buyer
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def delete_buyers(message: types.Message):
    if message.from_user.id in Director:
        if get_all_buyers():
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
            else:
                await message.answer("Список пуст!")

    else:
        await message.answer("Эта команда доступна только для директора!")


async def complete_delete_buyer(call: types.CallbackQuery):
    telegramm_id = int(call.data.replace("delete_staff", "").strip())

    await delete_buyer(telegramm_id)
    await call.message.delete()

    staff.remove(telegramm_id)
    with open('staff_config.py', 'w') as config_file:
        config_file.write(f"staff = {staff}")

    await call.message.answer(text="Байер удалён из базы данных")


def register_delete_staff(dp: Dispatcher):
    dp.register_message_handler(delete_buyers, commands=['Все_сотрудники'])
    dp.register_callback_query_handler(complete_delete_buyer,
                                       lambda call: call.data and call.data.startswith("delete_staff"))