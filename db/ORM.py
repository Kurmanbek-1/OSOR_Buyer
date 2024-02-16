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


async def get_all_buyers():
    async with asyncpg.create_pool(POSTGRES_URL) as pool:
        async with pool.acquire() as connection:
            rows = await connection.fetch("SELECT * FROM bayers")
            return rows


async def delete_buyer(telegramm_id):
    async with asyncpg.create_pool(POSTGRES_URL) as pool:
        async with pool.acquire() as connection:
            await connection.execute("DELETE FROM bayers WHERE telegramm_id = $1", telegramm_id)