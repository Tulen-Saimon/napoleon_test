from .models import offers


async def creat_offer(request):
    user_id, title, text = request.json.values()
    values = {'user_id': user_id, 'title': title, 'text': text}
    offer_query = offers.insert().values(**values)
    async with request.app.db_engine.acquire() as conn:
        async with conn.begin() as trans:
            try:
                await conn.execute(offer_query)
            except RuntimeError:
                await trans.rollback()
                return False
            else:
                await trans.commit()
                return True


async def get_offers(request):
    offer_id = list(request.json.values())
    where = offers.c.id == offer_id[0]
    offer_query = offers.select().where(where)
    async with request.app.db_engine.acquire() as conn:
        offer_raw = await (await conn.execute(offer_query)).fetchone()
        if offer_raw is None:
            return []
        else:
            return {'id': offer_raw.id, 'user_id': offer_raw.user_id, 'title': offer_raw.title, 'text': offer_raw.text}


async def get_user_offers(request):
    user_id = list(request.json.values())
    where = offers.c.user_id == user_id[0]
    user_query = offers.select().where(where)
    async with request.app.db_engine.acquire() as conn:
        user_raw = await (await conn.execute(user_query)).fetchall()
        if user_raw is None:
            return []
        else:
            res = list()
            for i in user_raw:
                res.append({'id': i.id, 'user_id': i.user_id, 'title': i.title, 'text': i.text})
            return res
