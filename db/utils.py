async def get_product_from_category(pool, category):
    try:
        async with pool.acquire() as connection:
            products = await connection.fetch(
                """SELECT * FROM orders
                WHERE category = $1""", category
            )
            return products
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return None


async def get_product_photos(pool, order_id):
    try:
        async with pool.acquire() as connection:
            photos = await connection.fetch(
                """SELECT * FROM photos_orders
                WHERE order_id = $1""", order_id
            )
            return photos
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return []

async def get_product_from_buyer_id(pool, buyer_id):
    try:
        async with pool.acquire() as connection:
            products = await connection.fetch(
                """SELECT * FROM orders
                WHERE bayer_id = $1""", buyer_id
            )
            return products
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return None