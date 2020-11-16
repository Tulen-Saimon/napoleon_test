from sqlalchemy import Column, String, MetaData, Table, Integer

metadata = MetaData()


users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(255)),
    Column('password', String(255)),
    Column('email', String(255))
)

users_create_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
    );
"""


async def create_tables(engine):
    async with engine.acquire() as conn:
        await conn.execute(users_create_query)
