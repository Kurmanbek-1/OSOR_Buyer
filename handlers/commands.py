from aiogram import Dispatcher, types
from config import Director
from staff_config import staff
import buttons


text = ('Добро пожаловать в наше творческое пространство, где каждый из вас играет важную роль в '
        'создании наших уникальных стилей. Мы - команда единомышленников, стремящихся '
        'к совершенству в мире моды. 💼'
        '\n'
        'Ваш вклад ценен, как ключевая составляющая успеха нашего бренда. '
        'Совместно мы формируем тренды, воплощаем идеи и делаем моду доступной для каждого.'
        '\n\n'
        'С благодарностью за ваш вклад в наш общий успех! 🚀✨'
        '\n\n')


async def start(message: types.Message):
    if message.from_user.id in Director:
        await message.answer(text=text)
        await message.answer(text='Вы директор ‼️', reply_markup=buttons.StartDirector)

    elif message.from_user in staff:
        await message.answer(text=text)
        await message.answer(text='Вы сотрудник ‼️', reply_markup=buttons.StartStaff)

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
    await message.answer(text='🛠️ Тех. поддержка:\n\n'
                              '📍Бишкек: +996221825236 \n'
                              '------------------------------\n'
                              '📍Ош: +996559618881 \n', reply_markup=buttons.StartClient)


async def support_for_admins(message: types.Message):
    if message.from_user.id in Director in staff:
        await message.answer('', reply_markup=buttons.StartAdmin)
    else:
        await message.answer('Вы не администратор или сотрудник!', reply_markup=buttons.StartClient)


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(support, commands=['ТехПоддержка', 'support'])
    dp.register_message_handler(support_for_admins, commands=['support'])
