from typing import Callable

from gino import Gino

db = Gino()


def init(db_url) -> Callable:
    """bind to database and create all tables"""

    async def f() -> None:
        await db.set_bind(db_url, isolation_level="READ COMMITTED", echo=False)
        await db.gino.create_all()

    return f


async def terminate() -> None:
    await db.pop_bind().close()
