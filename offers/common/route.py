from sanic import Blueprint as bp
from sanic.response import json
from common import functions


of = bp('offer', url_prefix='/offers')


@of.post('/create/')
async def creat_offer(request):
    if await functions.creat_offer(request):
        return json({'status': 'ok'}, status=201)
    else:
        return json({'error': 'Произошла ошибка добавления объявления'}, status=400)


@of.post('/')
async def get_user_offers(request):
    if 'user_id' in request.json:
        user_offers = await functions.get_user_offers(request)
        return json(user_offers)
    else:
        offers = await functions.get_offers(request)
        return json(offers)
