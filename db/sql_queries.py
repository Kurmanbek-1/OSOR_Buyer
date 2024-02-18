CREATE_TABLE_ORDER = '''
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        info TEXT,
        article TEXT UNIQUE,
        quantity INTEGER,
        category VARCHAR(255),
        price DECIMAL(10, 2),
        bayer_id TEXT,
        company_name VARCHAR(255)
    );
'''

ORDER_INSERT_QUERY = """
    INSERT INTO orders
    (info, article, quantity, category, price, bayer_id, company_name)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    ON CONFLICT DO NOTHING;
"""

CREATE_TABLE_PHOTO_OF_ORDERS = '''
    CREATE TABLE IF NOT EXISTS photos_orders (
        id SERIAL PRIMARY KEY,
        order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
        photo TEXT
    );
'''

ORDER_PHOTO_INSERT_QUERY = """
    INSERT INTO photos_orders
    (order_id, photo)
    VALUES ($1, $2)
    ON CONFLICT DO NOTHING;
"""


CREATE_TABLE_REVIEW = '''
    CREATE TABLE IF NOT EXISTS reviews (
        id SERIAL PRIMARY KEY,
        name_buyer VARCHAR(255),
        article_number TEXT,
        info_product TEXT,
        review TEXT
    );
'''

REVIEWS_INSERT_QUERY = """
    INSERT INTO reviews
    (name_buyer, article_number, info_product, review)
    VALUES ($1, $2, $3, $4)
    ON CONFLICT DO NOTHING;
"""

CREATE_TABLE_PHOTO_OF_REVIEWS = '''
    CREATE TABLE IF NOT EXISTS photos_review (
        id SERIAL PRIMARY KEY,
        review_id INTEGER REFERENCES reviews(id) ON DELETE CASCADE,
        photo TEXT
    );
'''

REVIEW_PHOTO_INSERT_QUERY = """
    INSERT INTO photos_review
    (review_id, photo)
    VALUES ($1, $2)
    ON CONFLICT DO NOTHING;
"""

CREATE_TABLE_BAYERS = """
    CREATE TABLE IF NOT EXISTS bayers (
        id SERIAL PRIMARY KEY,
        name_of_company VARCHAR(255),
        phone VARCHAR(255),
        fio TEXT,
        telegramm_id BIGINT UNIQUE
    );
"""

BAYERS_INSERT_QUERY = """
    INSERT INTO bayers
    (name_of_company, phone, fio, telegramm_id)
    VALUES ($1, $2, $3, $4)
    ON CONFLICT DO NOTHING;
"""

DELETE_PRODUCT_QUERY = """
    DELETE FROM orders WHERE id = $1;
"""

ALL_REVIEWS_FOR_DIRECTORS = """
    SELECT * FROM reviews
"""