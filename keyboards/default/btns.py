from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

send_phone_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(
        text='📲 Telefon raqamni yuborish!',
        request_contact=True
    )
)