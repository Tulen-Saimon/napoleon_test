import functools

import jwt
from sanic import Blueprint as bp
from sanic.response import json
from common import functions, settings

user = bp('user', url_prefix='/user')


def protected():
    def _protected(f):
        @functools.wraps(f)
        async def __protected(request, *args, **kwargs):
            # request = kwargs.get('request')
            if request.headers.get('Authorization'):
                token = request.headers.get('Authorization')
                if token.startswith('Bearer '):
                    token = token.replace('Bearer ', '')
                    try:
                        decoded = jwt.decode(token, settings.SECRET)
                    except jwt.DecodeError:
                        # Токен невалидный
                        return json({'error': 'Не правильный токен'}, status=401)
                    except jwt.ExpiredSignatureError:
                        # Токен стух
                        return json({'error': 'Время токена истекло'}, status=401)
                    else:
                        return await f(request, *args, **kwargs)
                else:
                    return json({'error': 'Неверный формат токена'}, status=401)
                    # Неправильный формат токена
            else:
                return json({'error': 'Токен отсутвует'}, status=401)
                # Отсутствует токен
        return __protected
    return _protected


@user.post('/registry/')
async def register_user(request):
    if await functions.create_user(request):
        return json({'status': 'ok'}, status=201)
    else:
        return json({'error': 'Произошла ошибка при регистрации пользователя'}, status=400)


@user.get('/<user_id>/')
@protected()
async def get_user(request, user_id):
    user = await functions.get_user(request, user_id)
    if user:
        return json(user)
    return json({'error': 'Пользователь не найден'})


@user.post('/auth/')
async def auth_user(request):
    token = await functions.authenticate_user(request)
    if token:
        return json({'token': token})
    else:
        return json({'error': 'Неправильный логин и/или пароль'}, status=401)
