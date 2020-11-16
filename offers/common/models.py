from sqlalchemy import Column, String, MetaData, Table, Integer, ForeignKey

metadata = MetaData()


offers = Table(
    'offers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('title', String(255)),
    Column('text', String(255))
)

users_create_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
    );
"""

offers_create_query = """
    CREATE TABLE IF NOT EXISTS offers (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title VARCHAR(255) NOT NULL,
        text VARCHAR(255) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
"""


async def create_tables(engine):
    async with engine.acquire() as conn:
        await conn.execute(offers_create_query)
