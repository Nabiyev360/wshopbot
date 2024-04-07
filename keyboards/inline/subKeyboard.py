from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db

def sub_keyboard(ctg_id):
    subs = db.select('products_subcategory', 'name', f'category_id = {ctg_id}')
    keyboard = InlineKeyboardMarkup()
    for sub in subs:
        keyboard.add(InlineKeyboardButton(sub[0], callback_data=sub[0]))
    keyboard.add(InlineKeyboardButton('🏠 Asosiy menyu', callback_data='main-menu'))

    return keyboard
