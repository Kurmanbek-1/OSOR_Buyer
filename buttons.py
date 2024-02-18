from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel_button = KeyboardButton('/Отмена❌')
cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True,
                                    ).add(cancel_button)

StartClient = ReplyKeyboardMarkup(resize_keyboard=True,
                                  one_time_keyboard=True,
                                  row_width=2
                                  ).add(KeyboardButton('/Товары!'),
                                        KeyboardButton('/ТехПоддержка'),
                                        KeyboardButton('/Написать_отзыв'),
                                        KeyboardButton('/Поиск'))

StartDirector = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True,
                                    row_width=2
                                    ).add(KeyboardButton('/Товары*'),
                                          KeyboardButton('/Все_сотрудники'),
                                          KeyboardButton('/Отзывы'),
                                          KeyboardButton('/Поиск'), )

StartStaff = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 row_width=2
                                 ).add(KeyboardButton('/Мои_товары!'),
                                       KeyboardButton('/Заполнить_товар!'),
                                       KeyboardButton('/Поиск'))


StartAdmin = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 row_width=2
                                 ).add(KeyboardButton('/Все_товары!'),
                                       KeyboardButton('/Поиск'))


cancel_for_client = ReplyKeyboardMarkup(resize_keyboard=True,
                                        one_time_keyboard=True,
                                        ).add(KeyboardButton('Отмена!'))

cancel_for_staff = ReplyKeyboardMarkup(resize_keyboard=True,
                                       one_time_keyboard=True,
                                       ).add(KeyboardButton('/Отмена!'))

cancel_for_director = ReplyKeyboardMarkup(resize_keyboard=True,
                                          one_time_keyboard=True,
                                          ).add(KeyboardButton('/Отмена🚫'))

CategoryButtonsStaff = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False,
                                           row_width=2).add(KeyboardButton('/Обувь'),
                                                            KeyboardButton('/Нижнее_белье'),
                                                            KeyboardButton('/Акссесуары'),
                                                            KeyboardButton('/Верхняя_одежда'),
                                                            KeyboardButton('/Штаны'),
                                                            KeyboardButton('/Отмена!'))

CategoryButtonsClient = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False,
                                            row_width=2).add(KeyboardButton('/Обувь'),
                                                             KeyboardButton('/Нижнее_белье'),
                                                             KeyboardButton('/Акссесуары'),
                                                             KeyboardButton('/Верхняя_одежда'),
                                                             KeyboardButton('/Штаны'),
                                                             KeyboardButton('Отмена!'))

CategoryButtonsAdmin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False,
                                            row_width=2).add(KeyboardButton('/Обувь'),
                                                             KeyboardButton('/Нижнее_белье'),
                                                             KeyboardButton('/Акссесуары'),
                                                             KeyboardButton('/Верхняя_одежда'),
                                                             KeyboardButton('/Штаны'),
                                                             KeyboardButton('/Отмена❌'))

finish_load_photos = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add \
    (KeyboardButton('/Сохранить_фотки!'))


submit_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True
                                    ).add(KeyboardButton('да'),
                                          KeyboardButton('нет'))