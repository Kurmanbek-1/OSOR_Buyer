from aiogram import Dispatcher, Bot
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db.db_bayer import Database


storage = MemoryStorage()
TOKEN = config('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


Director = [5818455846, ]
Admins = [6451475162, ]
Developers = [659106628, ]


ip = config('ip')
PostgresUser = config('PostgresUser')
PostgresPassword = config('PostgresPassword')
DATABASE = config('DATABASE')


POSTGRES_URL = f"postgresql://{PostgresUser}:{PostgresPassword}@{ip}/{DATABASE}"
data_base = Database(POSTGRES_URL)