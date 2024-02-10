from aiogram import Dispatcher, types
from config import Admins, Director
from staff_config import staff
import buttons


async def start(message: types.Message):
    if message.from_user.id in Admins:
        await message.answer('Приветствую, дорогие сотрудники OSOR-Factory! 🌟'
                             '\n\n'
                             'Добро пожаловать в наше творческое пространство, где каждый из вас играет важную роль в '
                             'создании наших уникальных стилей. Мы - команда единомышленников, стремящихся '
                             'к совершенству в мире моды. 💼'
                             '\n'
                             'Ваш вклад ценен, как ключевая составляющая успеха нашего бренда. '
                             'Совместно мы формируем тренды, воплощаем идеи и делаем моду доступной для каждого.'
                             '\n\n'
                             'С благодарностью за ваш вклад в наш общий успех! 🚀✨'
                             '\n\n'
                             'Вы админ ‼️',
                             reply_markup=buttons.StartAdmin)

    else:
        await message.answer('Приветствуем тебя в OSOR-Factory – твоем модном путеводителе в мире стиля! 🌟'
                             '\n\n'
                             'Здесь каждый образ – это уникальное творение, а наш склад стиля готов предложить тебе '
                             'лучшие тренды сезона.🛍️'
                             '\n\n'
                             'Закажи свой стиль прямо сейчас и ощути поток модных вдохновений, который приведет '
                             'твой гардероб к новым вершинам! 🚀✨',
                             reply_markup=buttons.StartClient)


async def support(message: types.Message):
    await message.answer('Наша тех.поддержка: ', reply_markup=buttons.StartClient)


async def support_for_admins(message: types.Message):
    if message.from_user.id in Admins:
        await message.answer('', reply_markup=buttons.StartAdmin)

    else:
        await message.answer('Вы не администратор или сотрудник!', reply_markup=buttons.StartClient)


async def Test_Staff(message: types.Message):
    if message.from_user.id in staff:
        await message.answer('Вы сотрудник!')
    else:
        await message.answer('Вы не сотрудник!')


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(support, commands=['ТехПоддержка'])
    dp.register_message_handler(support_for_admins, commands=['support'])
    dp.register_message_handler(Test_Staff, commands=['p'])
