import asyncpg
import asyncio

class Database:
    def __init__(self, dsn):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(self.dsn)
        except asyncpg.exceptions.TooManyConnectionsError:
            print("Too many connections. Retrying...")
            await asyncio.sleep(1)  # Подождать некоторое время перед повторной попыткой
            await self.connect()    # Повторить попытку подключения

    async def close(self):
        await self.pool.close()

    async def execute(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)
