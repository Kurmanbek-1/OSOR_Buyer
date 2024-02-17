from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, data_base, POSTGRES_URL
import buttons
import asyncpg

import random
import string

from staff_config import staff

from db.ORM import get_product_from_article, get_company_name, \
    insert_tovar, save_order_photo, get_last_inserted_order_id


# =======================================================================================================================

class FSM_fill_products(StatesGroup):
    info = State()
    quantity = State()
    category = State()
    price = State()
    photos = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in staff:
        await FSM_fill_products.info.set()
        await message.answer(text='Информация о товаре?!', reply_markup=buttons.cancel_for_staff)
    else:
        await message.answer('Вы не сотрудник!')


async def load_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info'] = message.text
    await FSM_fill_products.next()
    await message.answer(text='Количество товара?')



async def load_quantity(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['quantity'] = int(message.text)
        await FSM_fill_products.next()
        await message.answer(text='Категория товаров?', reply_markup=buttons.CategoryButtonsStaff)
    else:
        await message.answer('Введите числами!')


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text.replace("/", "")

    await FSM_fill_products.next()
    await message.answer(text="Цена товара?", reply_markup=buttons.cancel_for_staff)


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await FSM_fill_products.next()
    await message.answer(text="Отправьте фотографии", reply_markup=buttons.cancel_for_staff)


async def load_photos(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if "photos" in data:
            data["photos"].append(message.photo[-1].file_id)
        else:
            data["photos"] = [message.photo[-1].file_id]

    await message.answer(f"Добавлено!",
                         reply_markup=buttons.finish_load_photos)


async def generate_unique_article():
    article_length = 6
    while True:
        # Генерация случайного артикула из цифр
        article_number = ''.join(random.choices(string.digits, k=article_length))

        # Проверка наличия артикула в базе данных
        products = await get_product_from_article(article_number)
        if not products:
            return article_number  # Возвращаем уникальный артикул


async def finish_load_photos(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        telegramm_id = message.from_user.id
        company_name = await get_company_name(telegramm_id)

        data['company_name'] = company_name
        data['bayer_id'] = str(telegramm_id)

        article_number = await generate_unique_article()
        data['article'] = article_number

        product_info_text = (
            f"Байер: {data['company_name']}\n"
            f"Информация о товаре: {data['info']}\n"
            f"Артикул: {data['article']}\n"
            f"Количество: {data['quantity']}\n"
            f"Категория: {data['category']}\n"
            f"Цена: {data['price']}"
        )

        media_group = [types.InputMediaPhoto(media=image) for image in data['photos'][:-1]]
        last_image = data['photos'][-1]
        last_media = types.InputMediaPhoto(media=last_image, caption=product_info_text)
        media_group.append(last_media)

        await bot.send_media_group(chat_id=message.chat.id, media=media_group)

        await message.answer("Всё правильно?", reply_markup=buttons.submit_markup)
        await FSM_fill_products.next()


async def load_submit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "да":
            await data_base.connect()

            # Записываем информацию о товаре в таблицу products
            await insert_tovar(state)

            # Получаем ID последнего добавленного товара
            # Это нужно, чтобы привязать фотографии к данному товару
            order_id = await get_last_inserted_order_id()

            for photo in data['photos']:
                await save_order_photo(order_id, photo)

            await message.answer('Товар добавлен!', reply_markup=buttons.StartStaff)
            await state.finish()

            # Здесь можно добавить код для записи информации в базу данных,
            # если это требуется

        elif message.text.lower() == "нет":
            await message.answer('Отменено!', reply_markup=buttons.StartStaff)
            await state.finish()

        else:
            await message.answer("Пожалуйста, выберите Да или Нет.")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=buttons.StartStaff)


# =======================================================================================================================
def register_fill_products(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена!", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=["Заполнить_товар!"])

    dp.register_message_handler(load_info, state=FSM_fill_products.info)
    dp.register_message_handler(load_quantity, state=FSM_fill_products.quantity)
    dp.register_message_handler(load_category, state=FSM_fill_products.category)
    dp.register_message_handler(load_price, state=FSM_fill_products.price)

    dp.register_message_handler(load_photos, state=FSM_fill_products.photos, content_types=['photo'])
    dp.register_message_handler(finish_load_photos, state=FSM_fill_products.photos)
    dp.register_message_handler(load_submit, state=FSM_fill_products.submit)
