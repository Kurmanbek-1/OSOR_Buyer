from aiogram.utils import executor
import logging
from config import dp, bot, Developers
from handlers import commands
from handlers.FSM import registration
import buttons


# ===========================================================================
async def on_startup(_):
    for i in Developers:
        await bot.send_message(chat_id=i, text="Бот запущен!", reply_markup=buttons.StartAdmin)
        print('Бот начал работу!')

commands.register_commands(dp)
registration.registration(dp)

# ===========================================================================
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
