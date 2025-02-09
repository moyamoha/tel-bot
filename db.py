from tortoise import Tortoise
from di_container import AppContainer
from dependency_injector.wiring import inject, Provide
from dotmap import DotMap


@inject
async def init_db(config = Provide[AppContainer.config]):
    # Initialize the database connection
    conf = DotMap(config)
    # conn_name = conf.db.connections.for_bot_app
    await Tortoise.init(
        db_url=conf.db.url,  # Change this to your DB URL
        modules={"models": ["models.nooha", "models.category", "models.nooha_category"]},
        # connection_name=conn_name
    )
    await Tortoise.generate_schemas()