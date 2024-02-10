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

            print("База данных успешно подключена и таблицы созданы")
        finally:
            await pool.release(connection)