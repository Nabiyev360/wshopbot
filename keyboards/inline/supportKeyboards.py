from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

support_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('❎ Bekor qilish', callback_data='cancel-call'))
