from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import POSTGRES_URL, bot, Director, Admins
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import asyncpg
from keyboards import buttons
from staff_config import staff

from db.utils import get_product_from_category, get_product_photos

# =======================================================================================================================

class all_products_fsm(StatesGroup):
    category = State()
    more_tovars = State()


async def fsm_start(message: types.Message):
    user_id = message.from_user.id
    if user_id in staff or user_id in Director or user_id in Admins:
        await message.answer("Эта кнопка для клиентов!")
    else:
        await all_products_fsm.category.set()
        await message.answer(f"Категория товара?", reply_markup=buttons.CategoryButtonsClient)


"""Вывод категорий"""


async def load_category(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if user_id in Director or user_id in staff or user_id in Admins:
            await message.answer("Эта кнопка для клиентов")
        else:
            if message.text.startswith("/"):
                category = message.text.replace("/", "")
                pool = await asyncpg.create_pool(POSTGRES_URL, max_inactive_connection_lifetime=3)
                products = await get_product_from_category(pool, category)

                if products:
                    if len(products) <= 5:
                        for product in products:
                            product_info = (
                                f"Байер: {product['company_name']}\n"
                                f"Информация: {product['info']}\n"
                                f"Категория: {product['category']}\n"
                                f"Артикул: {product['article']}\n"
                                f"Количество: {product['quantity']}\n"
                                f"Цена: {product['price']}"
                            )

                            keyboard = InlineKeyboardMarkup().add(
                                InlineKeyboardButton(
                                    f"Заказать",
                                    callback_data=f"to_order{product['bayer_id']}"
                                )
                            )

                            photos = await get_product_photos(pool, product['id'])
                            photo_urls = [photo['photo'] for photo in photos]
                            media_group = [types.InputMediaPhoto(media=image) for image in photo_urls]

                            await bot.send_media_group(chat_id=message.chat.id, media=media_group)
                            await bot.send_message(chat_id=message.chat.id, text=product_info, reply_markup=keyboard)

                        await state.finish()
                        await message.answer(f"Это все товары из категории: {category}",
                                             reply_markup=buttons.StartClient)
                        await message.answer("Чтобы заказать товар нажмите на кнопку 'Заказать' под сообщением")
                    else:
                        chunks = [products[i:i + 5] for i in range(0, len(products), 5)]
                        data = await state.get_data()
                        current_chunk = data.get("current_chunk", 0)
                        current_products = chunks[current_chunk]

                        for product in current_products:
                            # Отправка информации о товаре
                            product_info = (
                                f"Байер: {product['company_name']}\n"
                                f"Информация: {product['info']}\n"
                                f"Категория: {product['category']}\n"
                                f"Артикул: {product['article']}\n"
                                f"Количество: {product['quantity']}\n"
                                f"Цена: {product['price']}"
                            )

                            keyboard = InlineKeyboardMarkup().add(
                                InlineKeyboardButton(
                                    f"Заказать",
                                    callback_data=f"to_order{product['bayer_id']}"
                                )
                            )

                            photos = await get_product_photos(pool, product['id'])
                            photo_urls = [photo['photo'] for photo in photos]
                            media_group = [types.InputMediaPhoto(media=image) for image in photo_urls]

                            await bot.send_media_group(chat_id=message.chat.id, media=media_group)
                            await bot.send_message(chat_id=message.chat.id, text=product_info, reply_markup=keyboard)

                        await state.update_data(current_chunk=current_chunk + 1)

                        if current_chunk < len(chunks) - 1:
                            ShowMore = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
                            ShowMore.add(KeyboardButton(f'Ещё из категории: {category}'))
                            ShowMore.add(KeyboardButton('Отмена!'))
                            await message.answer("Показать еще?", reply_markup=ShowMore)
                            await message.answer("Чтобы заказать товар, нажмите на кнопку (Отмена!), "
                                                 "либо выведите все товары до конца!")
                            await all_products_fsm.next()
                else:
                    await message.answer("В выбранной категории нет товаров")
            else:
                category = message.text.split()[-1]
                pool = await asyncpg.create_pool(POSTGRES_URL, max_inactive_connection_lifetime=3)
                products = await get_product_from_category(pool, category)

                if products:
                    chunks = [products[i:i + 5] for i in range(0, len(products), 5)]
                    data = await state.get_data()
                    current_chunk = data.get("current_chunk", 0)
                    current_products = chunks[current_chunk]

                    for product in current_products:
                        product_info = (
                            f"Байер: {product['company_name']}\n"
                            f"Информация: {product['info']}\n"
                            f"Категория: {product['category']}\n"
                            f"Артикул: {product['article']}\n"
                            f"Количество: {product['quantity']}\n"
                            f"Цена: {product['price']}"
                        )

                        keyboard = InlineKeyboardMarkup().add(
                            InlineKeyboardButton(
                                f"Заказать",
                                callback_data=f"to_order{product['bayer_id']}"
                            )
                        )

                        photos = await get_product_photos(pool, product['id'])
                        photo_urls = [photo['photo'] for photo in photos]
                        media_group = [types.InputMediaPhoto(media=image) for image in photo_urls]

                        await bot.send_media_group(chat_id=message.chat.id, media=media_group)
                        await bot.send_message(chat_id=message.chat.id, text=product_info, reply_markup=keyboard)
                    await state.update_data(current_chunk=current_chunk + 1)

                    if current_chunk < len(chunks) - 1:
                        ShowMore = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
                        ShowMore.add(KeyboardButton(f'Ещё из категории: {category}'))
                        ShowMore.add(KeyboardButton('Отмена!'))
                        await message.answer("Показать еще?", reply_markup=ShowMore)
                        await message.answer("Чтобы заказать товар, нажмите на кнопку (Отмена!), "
                                             "либо выведите все товары до конца!")
                        await all_products_fsm.more_tovars.set()
                    else:
                        await state.finish()
                        await message.answer(f"Это все товары из категории: {category}",
                                             reply_markup=buttons.StartClient)
                        await message.answer("Чтобы заказать товар нажмите на кнопку 'Заказать' под сообщением")
                else:
                    await message.answer("В выбранной категории нет товаров")
    except asyncpg.exceptions.TooManyConnectionsError:
        print("Many connections errors")


async def load_more(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await load_category(message, state)


async def cancel_reg(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in staff or user_id in Director or user_id in Admins:
        await message.answer("Эта кнопка для клиентов!")
    else:
        current_state = await state.get_state()
        if current_state is not None:
            await message.answer('Отменено!', reply_markup=buttons.StartClient)
            await state.finish()


# =======================================================================================================================
def register_all_products(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена!", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=["Товары!", 'all_products'])
    dp.register_message_handler(load_category, state=all_products_fsm.category)
    for category in ["Обувь", "Нижнее_белье", "Акссесуары", "Верхняя_одежда", "Штаны"]:
        dp.register_message_handler(load_more, Text(equals=f'Ещё из категории: {category}', ignore_case=True),
                                    state=all_products_fsm.more_tovars)