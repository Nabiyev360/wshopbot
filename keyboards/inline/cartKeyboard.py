from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


cart_btns = InlineKeyboardMarkup()
cart_btns.add(InlineKeyboardButton('📦 Xarid qilish', callback_data='buy'))
cart_btns.add(InlineKeyboardButton('❌ Savatni tozalash', callback_data='clear-cart'))
cart_btns.add(InlineKeyboardButton('🏠 Asosiy menyu', callback_data='main-menu'))


buy_btns = InlineKeyboardMarkup()
buy_btns.add(InlineKeyboardButton('🚚 Yetkazib berish', callback_data='buy-type-deliver'))
buy_btns.add(InlineKeyboardButton('📦 Dokondan olib ketish', callback_data='buy-type-from-shop'))
buy_btns.add(InlineKeyboardButton('🔙 Orqaga', callback_data='back_to_cart'))


pay_type_btns = InlineKeyboardMarkup()
pay_type_btns.add(InlineKeyboardButton('📱 Click', callback_data='click'))
pay_type_btns.add(
    InlineKeyboardButton('🅿️ PayMe', callback_data='payme'),
    InlineKeyboardButton('🍋️ Qiwi', callback_data='payme'),
)
pay_type_btns.add(InlineKeyboardButton('💵 Naqd pul', callback_data='naqd-pul'))
pay_type_btns.add(InlineKeyboardButton('🔙 Orqaga', callback_data='back_to_type_pay'))
