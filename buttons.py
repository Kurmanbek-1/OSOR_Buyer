from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel_button = KeyboardButton('Отмена')
cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True,
                                    ).add(cancel_button)

StartAdmin = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 row_width=2).add(KeyboardButton(''))
