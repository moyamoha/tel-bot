from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from dependency_injector.wiring import Provide, inject
from di_container import AppContainer
from models.nooha import Nooha
from models.category import Category
from services.nooha_storage import NoohaStorage

welcome_text = '''
          سلام کاربر گرامی! به ربات @یا_حسین خوش آمدید. اینجا میتونید کلی نوحه و مداحی های متنوع و گوناگون دانلود کنید. لطفا یکی از مجموعه های زیر را انتخاب کنید   
        '''

@inject
async def start(
        update: Update,
        context: ContextTypes = ContextTypes.DEFAULT_TYPE,
        nooha_storage: NoohaStorage = Provide[AppContainer.nooha_storage]
    ):
    parts = update.message.text.split(' ')
    if len(parts) == 2:
        if parts[1].startswith('get_nooha_'):
            nooha_id = int(parts[1].split('_')[-1])
            found_nooha = await Nooha.get(id=nooha_id)
            if not found_nooha:
                await update.message.reply_text(text="Resourse not found")
            else:
                url = nooha_storage.get_public_nooha_url(found_nooha)
                if url == '':
                    await update.message.reply_text(text="Resourse not found")
                else:
                    await update.message.reply_document(document=url)
    else:
        try:
            categories = await Category.all()
            keyboard = []
            for c in categories:
                keyboard.append(
                    [InlineKeyboardButton(f"{c.title}", callback_data=f"get_noohas_for:{c.title}")]
                )
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                text=welcome_text,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
        except Exception as e:
            print(e)