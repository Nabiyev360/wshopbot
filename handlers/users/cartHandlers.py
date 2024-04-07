from aiogram import types
from aiogram.dispatcher import FSMContext
from asyncio import sleep

from loader import dp, db
from keyboards.inline.cartKeyboard import cart_btns, buy_btns
from keyboards.default.mainKeyboard import main_keyboard, cancel_btn
from states.buyStates import BuytState


@dp.message_handler(text='🛒 Savat')
async def cart_handler(msg: types.Message):
    user_id = msg.from_user.id
    session = db.select('accounts_shoppingsession', 'session_id', f'user_id={user_id} AND status!=3')

    if not session:
        await msg.answer("📤 Savat bo'sh", reply_markup=main_keyboard())
        return

    user_current_session = session[0][0]
    cart_products_data = db.select('accounts_cartitem', 'product_id, quantity', f'session_id={user_current_session}')

    if not cart_products_data:
        await msg.answer("📤 Savat bo'sh", reply_markup=main_keyboard())
        return

    quantities = []
    for products_data in cart_products_data:
        quantities.append(products_data[1])
    quantities = list(reversed(quantities))

    cart_products = []
    for product_id in cart_products_data:
        cart_products.append(
            db.select('products_product', 'title, price, subcategory_id', f'id={product_id[0]}')[0]
        )

    txt = ''
    total_price = 0

    for product in cart_products:
        title = product[0]
        price = product[1]

        quantity = quantities.pop()

        txt += f'<b>{title} x {quantity}</b>\n'
        txt += f"<code>{price} x {quantity} = {price * quantity} so'm</code>\n\n"

        total_price += price * quantity

    txt += f"\nJami: {total_price} so'm"

    await msg.answer(txt, reply_markup=cart_btns)


@dp.callback_query_handler(text='shopping_cart')
async def cart_callback_handler(call: types.CallbackQuery):
    user_id = call.from_user.id

    session = db.select('accounts_shoppingsession', 'session_id', f'user_id={user_id} AND status!=3')

    if not session:
        await call.answer("Savat bo'sh")
        return

    user_current_session = session[0][0]
    cart_products_data = db.select('accounts_cartitem', 'product_id, quantity', f'session_id={user_current_session}')

    if not cart_products_data:
        await call.answer("Savat bo'sh")
        return

    quantities = []
    for products_data in cart_products_data:
        quantities.append(products_data[1])
    quantities = list(reversed(quantities))

    cart_products = []
    for product_id in cart_products_data:
        cart_products.append(
            db.select('products_product', 'title, price, subcategory_id', f'id={product_id[0]}')[0]
        )

    txt = ''
    total_price = 0

    for product in cart_products:
        title = product[0]
        price = product[1]

        quantity = quantities.pop()

        txt += f'<b>{title} x {quantity}</b>\n'
        txt += f"<code>{price} x {quantity} = {price * quantity} so'm</code>\n\n"

        total_price += price * quantity

    txt += f"\nJami: {total_price} so'm"

    await call.message.edit_text(text=txt, reply_markup=cart_btns)
    await call.answer()


@dp.callback_query_handler(text='buy')
async def buy_handler(call: types.CallbackQuery):
    await call.message.edit_text("Buyurtma turini tanlang:", reply_markup=buy_btns)


@dp.callback_query_handler(text='buy-type-deliver')
async def buy_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await dp.bot.send_message(
        chat_id=call.from_user.id,
        text="<b>Yetkazib berish manzilini jonating.</b> <i>Tuman, ko'cha, uy raqami, xonadon</i>",
        reply_markup=cancel_btn
    )

    await BuytState.waiting_location.set()



@dp.callback_query_handler(text='clear-cart')
async def cart_callback_handler(call: types.CallbackQuery):
    session_id = db.select('accounts_shoppingsession', 'session_id', f'user_id={call.from_user.id} AND status!=3')[0][0]
    db.delete('accounts_cartitem', f'session_id={session_id}')

    await call.answer('✅ Savat tozalandi!')
    await call.message.edit_text('📂')
    await call.message.answer('Asosiy menyu', reply_markup=main_keyboard())
    await sleep(3)
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
