CREATE_TABLE_ORDER = '''
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        bayer_id VARCHAR(255) UNIQUE,
        article TEXT UNIQUE,
        company_name VARCHAR(255),
        bayer_datas TEXT,
        category VARCHAR(255),
        price DECIMAL(10, 2)
    );
'''

ORDER_INSERT_QUERY = """
    INSERT INTO orders
    (bayer_id, article_number, company_name, bayer_datas, category, price)
    VALUES ($1, $2, $3, $4, $5, $6)
    ON CONFLICT DO NOTHING;
"""

CREATE_TABLE_PHOTO_OF_ORDERS = '''
    CREATE TABLE IF NOT EXISTS photos (
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
        article TEXT,
        name_order TEXT,
        name_bayer VARCHAR(255),
        text_review TEXT
    );
'''

REVIEWS_INSERT_QUERY = """
    INSERT INTO reviews
    (article, name_order, name_bayer, text_review)
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
    INSERT INTO photos_orders
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
        telegramm_id TEXT UNIQUE
    );
"""

BAYERS_INSERT_QUERY = """
    INSERT INTO bayers
    (name_of_company, phone, fio, telegramm_id)
    VALUES ($1, $2, $3, $4)
    ON CONFLICT DO NOTHING;
"""