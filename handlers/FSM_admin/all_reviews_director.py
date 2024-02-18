from aiogram import types, Dispatcher
from config import POSTGRES_URL, bot, Director, Admins
from db.ORM import get_all_reviews
from db.utils import get_review_photos

import asyncpg
from keyboards import buttons


async def reviews_for_directors(message: types.Message):
    if message.from_user.id in Director:
        pool = await asyncpg.create_pool(POSTGRES_URL)
        reviews = await get_all_reviews(pool)

        if reviews:
            for review in reviews:
                review_info = (
                    f"Байер: {review['name_buyer']}\n"
                    f"Артикул товара: {review['article_number']}\n"
                    f"Название товара: {review['info_product']}\n"
                    f"Отзыв: {review['review']}/5"
                )

                photos = await get_review_photos(pool, review['id'])

                if photos:
                    photo_urls = [photo['photo'] for photo in photos]

                    media_group = [types.InputMediaPhoto(media=image) for image in photo_urls[:-1]]

                    last_image = photo_urls[-1]
                    last_media = types.InputMediaPhoto(media=last_image, caption=review_info)

                    media_group.append(last_media)

                    await bot.send_media_group(chat_id=message.chat.id, media=media_group)
                else:
                    await message.answer(review_info, reply_markup=buttons.StartDirector)
    elif message.from_user.id in Admins:
        await message.answer('Вы не директор!', reply_markup=buttons.StartAdmin)
    else:
        await message.answer('Вы не директор!', reply_markup=buttons.StartClient)


def register_all_reviews_for_directors(dp: Dispatcher):
    dp.register_message_handler(reviews_for_directors, commands=["Отзывы", 'all_reviews_director'])