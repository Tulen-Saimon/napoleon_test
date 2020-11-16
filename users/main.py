from sanic import Sanic
from sanic.response import json
from sanic_openapi import swagger_blueprint
from aiopg.sa import create_engine
from common import settings
from common import functions
from common.models import create_tables
from common.route import user


app = Sanic('users_service')
app.blueprint(swagger_blueprint)
app.blueprint(user)


def setup_database():
    db_settings = {
        'SQL_DB_HOST': settings.SQL_DB_HOST,
        'SQL_DB_PORT': settings.SQL_DB_PORT,
        'SQL_DB_NAME': settings.SQL_DB_NAME,
        'SQL_DB_USER': settings.SQL_DB_USER,
        'SQL_DB_PASSWORD': settings.SQL_DB_PASSWORD
    }
    app.config.update(db_settings)

    connection = f'postgres://{app.config.SQL_DB_USER}:{app.config.SQL_DB_PASSWORD}@{app.config.SQL_DB_HOST}:{app.config.SQL_DB_PORT}/{app.config.SQL_DB_NAME}'

    @app.listener('after_server_start')
    async def connect_to_db(*args, **kwargs):
        app.db_connection = connection
        app.db_engine = await create_engine(connection)
        await create_tables(app.db_engine)


def main():
    setup_database()
    app.run(host='0.0.0.0', port=8000, debug=True)


if __name__ == '__main__':
    main()
