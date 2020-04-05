from starlette.applications import Starlette
from api.engine import init, terminate
import asyncio
import logging
from api import periodic
from api.routes import routes, middleware
from api.settings import Settings, SettingsDev, build_pg_url

logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)


def background_task(settings: Settings) -> None:
    logging.info("background task is running")
    asyncio.ensure_future(periodic.every_nsec(settings))


def create_app(settings: Settings, debug=False) -> Starlette:
    """Application factory
    setup: routes, database(engine, create tables), periodic background task"""
    database_url = build_pg_url(settings)
    app = Starlette(debug=debug, routes=routes, middleware=middleware,
                    on_startup=[init(database_url), lambda: background_task(settings)],
                    on_shutdown=[terminate]
                    )
    logging.info("Twitter Starlette app is running")
    return app


dev_app = create_app(SettingsDev(), debug=True)
prod_app = create_app(Settings())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(dev_app, host="0.0.0.0", port=8000)
