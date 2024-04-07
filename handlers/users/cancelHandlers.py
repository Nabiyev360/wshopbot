from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.mainKeyboard import main_keyboard
from keyboards.inline.cartKeyboard import buy_btns, cart_btns
from loader import dp, db


@dp.message_handler(text='↩ Orqaga', state='*')
async def main_menu_handler(msg: types.Message, state: FSMContext):
    await msg.answer('Buyurtna turini tanlang:', reply_markup=buy_btns)
    await state.finish()


@dp.message_handler(text='✖ Bekor qilish', state='*')
async def main_menu_handler(msg: types.Message, state: FSMContext):
    await msg.answer('Asosiy menyu', reply_markup=main_keyboard())
    await state.finish()


@dp.callback_query_handler(text='back_to_cart', state='*')
async def main_menu_handler(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    session = db.select('accounts_shoppingsession', 'session_id', f'user_id={user_id} AND status!=3')

    if not session:
        await call.message.delete()
        await call.message.answer("📤 Savat bo'sh", reply_markup=main_keyboard())
        return

    user_current_session = session[0][0]
    cart_products_data = db.select('accounts_cartitem', 'product_id, quantity', f'session_id={user_current_session}')

    if not cart_products_data:
        await call.message.delete()
        await call.message.answer("📤 Savat bo'sh", reply_markup=main_keyboard())
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

    await call.message.edit_text(txt, reply_markup=cart_btns)