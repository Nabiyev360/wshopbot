from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


def detail_keyboard(pr_title, subctg_name):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("📥 Savatga qo'shish", callback_data=f'buy_pr:{pr_title}'))
    keyboard.add(InlineKeyboardButton("⬅ Orqaga", callback_data=f'{subctg_name}'))
    return keyboard


def next_add(next_count=1, subctg_name='?'):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("-1", callback_data='del_again'),
        # InlineKeyboardButton(f"🛍 {next_count} dona", callback_data=str(next_count)),
        InlineKeyboardButton(f"🛍 {next_count} dona", callback_data=f'pr_count={next_count}'),
        InlineKeyboardButton("+1", callback_data='add_again')
    )
    keyboard.add(
        InlineKeyboardButton("⬅ Orqaga", callback_data=subctg_name),
        InlineKeyboardButton("🛒 Savat", callback_data='shopping_cart')
    )
    return keyboard
