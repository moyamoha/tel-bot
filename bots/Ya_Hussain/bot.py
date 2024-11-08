from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from dependency_injector.wiring import inject, Provide
from di_container import AppContainer
from dotmap import DotMap
from bots.Ya_Hussain.handlers import callback_handlers, start_command


@inject
def create_yahya_salimi_bot(config = Provide[AppContainer.config]):
    conf = DotMap(config)
    app = ApplicationBuilder().token(conf.telegram.bots.ya_hussain_313.token).build()
    app.add_handler(CommandHandler("start", start_command.start))
    app.add_handler(CallbackQueryHandler(callback=callback_handlers.list_noohas, pattern=r"^get_noohas_for:"))
    return app