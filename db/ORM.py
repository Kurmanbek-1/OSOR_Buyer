import asyncpg
from db import sql_queries
from config import POSTGRES_URL


async def create_tables():
    global pool
    pool = await asyncpg.create_pool(POSTGRES_URL)
    async with pool.acquire() as connection:
        try:
            await connection.execute(sql_queries.CREATE_TABLE_ORDER)
            await connection.execute(sql_queries.CREATE_TABLE_PHOTO_OF_ORDERS)
            await connection.execute(sql_queries.CREATE_TABLE_REVIEW)
            await connection.execute(sql_queries.CREATE_TABLE_PHOTO_OF_REVIEWS)
            await connection.execute(sql_queries.CREATE_TABLE_BAYERS)

            print("База данных успешно подключена и таблицы созданы")
        finally:
            await pool.release(connection)


async def insert_bayers(name_of_company, phone, fio, telegramm_id):
    async with pool.acquire() as connection:
        values = (
            name_of_company,
            phone,
            fio,
            telegramm_id,
        )
        await connection.execute(sql_queries.BAYERS_INSERT_QUERY, *values)


async def check_telegramm_id_existence(telegramm_id):
    async with pool.acquire() as connection:
        existing_user = await connection.fetchval(
            "SELECT COUNT(*) FROM bayers WHERE telegramm_id = $1", telegramm_id
        )
        # Если пользователь с таким telegramm_id уже зарегистрирован, возвращаем True
        return existing_user > 0


async def check_company_name_existence(company_name):
    async with pool.acquire() as connection:
        existing_company = await connection.fetchval(
            "SELECT COUNT(*) FROM bayers WHERE name_of_company = $1", company_name
        )
        # Если пользователь с таким telegramm_id уже зарегистрирован, возвращаем True
        return existing_company > 0


async def get_all_buyers():
    async with asyncpg.create_pool(POSTGRES_URL) as pool:
        async with pool.acquire() as connection:
            rows = await connection.fetch("SELECT * FROM bayers")
            return rows


async def get_company_name(telegramm_id):
    async with pool.acquire() as connection:
        company = await connection.fetchval(
            "SELECT name_of_company FROM bayers WHERE telegramm_id = $1", telegramm_id
        )

        return company


async def get_product_from_article(article):
    async with asyncpg.create_pool(POSTGRES_URL) as pool:
        async with pool.acquire() as connection:
            products = await connection.fetch(
                """SELECT * FROM orders
                WHERE article = $1""", article
            )

            return products


async def delete_buyer(telegramm_id):
    async with asyncpg.create_pool(POSTGRES_URL) as pool:
        async with pool.acquire() as connection:
            await connection.execute("DELETE FROM bayers WHERE telegramm_id = $1", telegramm_id)


async def insert_tovar(state):
    async with pool.acquire() as connection:
        async with state.proxy() as data:
            values = (
                data['info'],
                data['article'],
                data['quantity'],
                data['category'],
                data['price'],
                data['bayer_id'],
                data['company_name'],
            )
            await connection.execute(sql_queries.ORDER_INSERT_QUERY, *values)


async def save_order_photo(order_id, photo):
    async with pool.acquire() as connection:
        values = (
            order_id,
            photo,
        )
        await connection.execute(sql_queries.ORDER_PHOTO_INSERT_QUERY, *values)


async def get_last_inserted_order_id():
    async with pool.acquire() as connection:
        return await connection.fetchval("SELECT lastval()")


async def delete_product(product_id):
    product_id = int(product_id)
    async with pool.acquire() as connection:
        await connection.execute(sql_queries.DELETE_PRODUCT_QUERY, product_id)

        await connection.execute("""DELETE FROM orders WHERE id = $1;""", product_id)


async def insert_reviews(state):
    async with pool.acquire() as connection:
        async with state.proxy() as data:
            values = (
                data['name_buyer'],
                data['article_number'],
                data['info_product'],
                data['review'],
            )
            await connection.execute(sql_queries.REVIEWS_INSERT_QUERY, *values)


async def save_review_photo(review_id, photo):
    async with pool.acquire() as connection:
        values = (
            review_id,
            photo,
        )
        await connection.execute(sql_queries.REVIEW_PHOTO_INSERT_QUERY, *values)


async def get_last_inserted_review_id():
    async with pool.acquire() as connection:
        return await connection.fetchval("SELECT lastval()")


async def get_all_reviews(pool):
    async with pool.acquire() as connection:
        return await connection.fetch(sql_queries.ALL_REVIEWS_FOR_DIRECTORS)
