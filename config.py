from aiogram import Dispatcher, Bot
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

TOKEN = config('TOKEN')

Admins = [995712956, ]
Director = [6451475162, ]

Developers = [995712956, ]

bot = Bot(TOKEN)

dp = Dispatcher(bot=bot, storage=storage)

staff = []
staff.append(995712956)
