from aiogram.utils import executor
import logging
import buttons
from config import dp, bot, Developers, data_base

from handlers import commands, search
from handlers.FSM_admin import registration
from handlers.FSM_client import all_products_client, order_client, review_client
from handlers.FSM_staff import all_products_staff, fill_products_staff

from db.ORM import create_tables


# ===========================================================================
async def on_startup(_):
    for i in Developers:
        await bot.send_message(chat_id=i, text="Бот запущен!", reply_markup=buttons.StartStaff)
        print('Бот начал работу!')
    await data_base.connect()
    await create_tables()


commands.register_commands(dp)
search.register_search(dp)

registration.registration(dp)
review_client.register_review(dp)

order_client.register_order_for_client(dp)
all_products_client.register_all_products(dp)

all_products_staff.register_all_products_admins(dp)
fill_products_staff.register_fill_products(dp)

# ===========================================================================
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)