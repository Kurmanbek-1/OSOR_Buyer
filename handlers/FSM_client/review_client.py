from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from staff_config import staff
from keyboards import buttons
from datetime import datetime
from config import Admins, bot, Director

from db.ORM import insert_reviews, get_last_inserted_review_id, save_review_photo


# ======================================================================================================================


class review_fsm(StatesGroup):
    name_buyer = State()
    articule = State()
    name = State()
    review = State()
    submit_photo = State()
    photo = State()
    finish_photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in staff or message.from_user.id in Admins or \
            message.from_user.id in Director:
        await message.answer('Вы сотдруник, вы не можете оcтавить отзыв!')
    else:
        await review_fsm.name_buyer.set()
        await message.answer(text="Название байеров?", reply_markup=buttons.cancel_for_client)


async def load_name_buyer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name_buyer"] = message.text
    await review_fsm.next()
    await message.answer("Артикул товара!?")


async def load_articule(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["article_number"] = message.text
    await review_fsm.next()
    await message.answer("Название товара!?")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["info_product"] = message.text
    await review_fsm.next()
    await message.answer("Отзыв о товаре!?\n" "?/5")


async def load_review(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["review"] = message.text
    await review_fsm.next()
    await message.answer("Вы хотите отправить фото товара?", reply_markup=buttons.submit_markup)


async def submit_photo(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await review_fsm.next()
        await message.answer("Отправьте фотку товара")
    elif message.text.lower() == 'нет':
        async with state.proxy() as data:
            data["photo_review"] = None
            await message.answer(f"Артикуль товара: {data['article_number']}\n"
                                 f"Название товара: {data['info_product']}\n"
                                 f"Отзыв о товаре: {data['review']}\n")
            await review_fsm.submit.set()
            await message.answer("Все верно?", reply_markup=buttons.submit_markup)
    else:
        await message.answer("Пожалуйста, выберите Да или Нет.", reply_markup=buttons.submit_markup)


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if "photo_review" in data:
            data["photo_review"].append(message.photo[-1].file_id)
        else:
            data["photo_review"] = [message.photo[-1].file_id]

    await message.answer(f"Добавлено!",
                         reply_markup=buttons.finish_load_photos)
    await review_fsm.finish_photo.set()

async def finish_load_photos(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        review_text = (
            f"Данные товара: \n"
            f"Байера: {data['name_buyer']}\n"
            f"Артикуль товара: {data['article_number']}\n"
            f"Название товара: {data['info_product']}\n"
            f"Отзыв о товаре: {data['review']}\n"
        )

        media_group = [types.InputMediaPhoto(media=image) for image in data['photo_review'][:-1]]
        last_image = data['photo_review'][-1]
        last_media = types.InputMediaPhoto(media=last_image, caption=review_text)
        media_group.append(last_media)

        await bot.send_media_group(chat_id=message.chat.id, media=media_group)

        await review_fsm.next()
        await message.answer("Все верно?", reply_markup=buttons.submit_markup)


async def load_submit(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        async with state.proxy() as data:
            if data['photo_review'] is None:
                await insert_reviews(state)
                await message.answer('Готово!', reply_markup=buttons.StartClient)
                await state.finish()
            else:
                await insert_reviews(state)

                review_id = await get_last_inserted_review_id()

                for photo in data['photo_review']:
                    await save_review_photo(review_id, photo)

                await message.answer('Готово!', reply_markup=buttons.StartClient)
                await state.finish()
    elif message.text.lower() == 'нет':
        await message.answer('Хорошо, отменено', reply_markup=buttons.StartClient)
        await state.finish()
    else:
        await message.answer("Пожалуйста, выберите Да или Нет.")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=buttons.StartClient)


# ======================================================================================================================

def register_review(dp: Dispatcher):
    dp.register_message_handler(
        cancel_reg, Text(equals="/cancel", ignore_case=True), state="*"
    )
    dp.register_message_handler(fsm_start, commands=["Написать_отзыв", "review"])

    dp.register_message_handler(load_name_buyer, state=review_fsm.name_buyer)
    dp.register_message_handler(load_articule, state=review_fsm.articule)
    dp.register_message_handler(load_name, state=review_fsm.name)
    dp.register_message_handler(load_review, state=review_fsm.review)
    dp.register_message_handler(submit_photo, state=review_fsm.submit_photo)
    dp.register_message_handler(load_photo, state=review_fsm.photo, content_types=["photo"])
    dp.register_message_handler(finish_load_photos, state=review_fsm.finish_photo)
    dp.register_message_handler(load_submit, state=review_fsm.submit)
