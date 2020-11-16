from .models import users
from bcrypt import hashpw, gensalt, checkpw
from .settings import SECRET
import jwt
from datetime import datetime, timedelta
from sqlalchemy import and_
import aiohttp
import asyncio
import async_timeout


async def get_user(request, user_id):
    offers = await get_offers(user_id)
    where = users.c.id == user_id
    user_query = users.select().where(where)
    async with request.app.db_engine.acquire() as conn:
        user_raw = await (await conn.execute(user_query)).fetchone()
        if user_raw is None:
            return False

    return {'id': user_raw.id, 'username': user_raw.username, 'email': user_raw.email, 'offers': offers}


async def create_user(request):
    username, password, email = request.json.values()
    if not await check_login(request.app.db_engine, username):
        return False
    values = {'username': username, 'password': hash_password(password), 'email': email}
    user_query = users.insert().values(**values)
    async with request.app.db_engine.acquire() as conn:
        async with conn.begin() as trans:
            try:
                await conn.execute(user_query)
            except RuntimeError:
                await trans.rollback()
                return False
            else:
                await trans.commit()
                return True


def hash_password(password):
    return hashpw(password.encode(), gensalt()).decode('utf-8')


def generate_jwt(username):
    return jwt.encode({'username': username, 'exp': datetime.utcnow() + timedelta(hours=1)}, SECRET, algorithm='HS256')


async def check_credentials(engine, username, password):
    where = and_(users.c.username == username)
    user_query = users.select().where(where)
    async with engine.acquire() as conn:
        user = await (await conn.execute(user_query)).fetchone()
        if user is None:
            return False
        return checkpw(password.encode(), user.password.encode())


async def authenticate_user(request):
    if await check_credentials(request.app.db_engine, request.json.get('username'), request.json.get('password')):
        return generate_jwt(request.json.get('username')).decode('utf-8')
    else:
        return False


async def get_offers(user_id):
    req_json = {'user_id': user_id}
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8001/offers/', json=req_json) as resp:
            return await resp.text()


async def check_login(engine, username):
    where = users.c.username == username
    user_query = users.select().where(where)
    async with engine.acquire() as conn:
        user = await (await conn.execute(user_query)).fetchone()
        if user is None:
            return True
