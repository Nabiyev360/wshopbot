from aiogram.types import ReplyKeyboardMarkup

from loader import db


def main_keyboard():
    categories = db.select('products_category', 'name')
    k = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for ctg in categories:
        ctg_name = ctg[0]
        if len(ctg_name) < 13:
            k.insert(ctg_name)
        else:
            k.add(ctg_name)

    k.add('🛒 Savat', '📲 Murojaat uchun')

    return k

cancel_btn = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).add('↩ Orqaga', ' ✖ Bekor qilish')