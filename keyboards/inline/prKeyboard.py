from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


def pr_keyboard(products, sub_name):
    keyboard = InlineKeyboardMarkup()
    for pr in products:
        keyboard.add(InlineKeyboardButton(pr[0], callback_data=pr[0]))

    keyboard.add(InlineKeyboardButton("⬅ Orqaga", callback_data=sub_name))

    return keyboard
