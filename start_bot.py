import threading
from typing import Final
from bots.Ya_Hussain.bot import create_yahya_salimi_bot
from db import init_db
from di_container import AppContainer
import asyncio

BOT_DB_CONNECTION_NAME: Final = "bot_db_conn"

def start_bot():
    app = create_yahya_salimi_bot()
    print('BOT @Ya_Hussain_313_bot is running ...')
    app.run_polling()

if __name__ == '__main__':
    container = AppContainer()
    container.init_resources()
    container.wire(packages=["bots.Ya_Hussain", "bots.Ya_Hussain.handlers"], modules=["db"])
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_db())
    
    start_bot()