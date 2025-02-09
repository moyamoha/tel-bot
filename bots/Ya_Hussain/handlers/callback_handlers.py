from dotmap import DotMap
from telegram import Update
from telegram.ext import ContextTypes
from di_container import AppContainer
from models.category import Category
from models.nooha import Nooha
from dependency_injector.wiring import inject, Provide


@inject
async def list_noohas(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        config = Provide[AppContainer.config]
    ):
    query = update.callback_query
    await query.answer()
    conf = DotMap(config)
    bot_url = f"https://t.me/{conf.telegram.bots.ya_hussain_313.username}"
    # Extract URL from callback data
    category_title = query.data.split(':')[1]
    category = await Category.get(title=category_title)
    noohas = await Nooha.filter(categories=category).prefetch_related('categories').order_by('title')
    text = f"نوحه ها و مداحی های با موضوع <strong>{category_title}:</strong>\n\n"
    for i, n in enumerate(noohas):
        # title = escape_markdown(n.title)
        text += f"<a href='{bot_url}?start=get_nooha_{n.id}'>{i+1}: {n.title}</a>\n\n"

    await context.bot.send_message(
        update.effective_chat.id,
        text=text,
        parse_mode="HTML"
    )

