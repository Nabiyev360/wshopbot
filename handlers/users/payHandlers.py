from aiogram import types

from loader import bot, dp, db
from data.config import ADMINS
from data.products import python_book, cart_objects, ds_praktikum,  FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING
from keyboards.default.mainKeyboard import main_keyboard


@dp.callback_query_handler(text="click")
async def book_invoice(call: types.CallbackQuery):
    user_id = call.from_user.id
    session = db.select('accounts_shoppingsession', 'session_id', f'user_id={user_id} AND status!=3')

    if not session:
        await call.answer("📤 Savat bo'sh", show_alert=True)
        await call.message.answer('Asosiy menyu', reply_markup=main_keyboard())
        await call.message.delete()
        return

    user_current_session = session[0][0]
    cart_products_data = db.select('accounts_cartitem', 'product_id, quantity', f'session_id={user_current_session}')

    if not cart_products_data:
        await call.answer("📤 Savat bo'sh", show_alert=True)
        await call.message.answer('Asosiy menyu', reply_markup=main_keyboard())
        await call.message.delete()
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

    # txt = ''
    # total_price = 0

    # for product in cart_products:
    #     title = product[0]
    #     price = product[1]
    #
    #     quantity = quantities.pop()
    #
    #     txt += f'<b>{title} x {quantity}</b>\n'
    #     txt += f"<code>{price} x {quantity} = {price * quantity} so'm</code>\n\n"
    #
    #     total_price += price * quantity

    # txt += f"\nJami: {total_price} so'm"

    objects = cart_objects(cart_products, quantities).generate_invoice()

    await bot.send_invoice(chat_id=call.from_user.id,
                           **objects,
                           payload="payload:test")
    await call.answer()
    await call.message.answer('Asosiy menyu', reply_markup=main_keyboard())
    await call.message.delete()




@dp.shipping_query_handler()
async def choose_shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code != "UZ":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message="Chet elga yetkazib bera olmaymiz")
    elif query.shipping_address.city.lower() == "tashkent":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGULAR_SHIPPING],
                                        ok=True)



@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Buyurtmangiz qabul qilindi. Xaridingiz uchun rahmat!")
    await bot.send_message(chat_id=ADMINS[0],
                           text=f"Quyidagi mahsulot sotildi: {pre_checkout_query.invoice_payload}\n"
                                f"ID: {pre_checkout_query.id}\n"
                                f"Telegram user: {pre_checkout_query.from_user.first_name}\n"                                
                                f"Xaridor: {pre_checkout_query.order_info.name}, tel: {pre_checkout_query.order_info.phone_number}")

    session_id = db.select('accounts_shoppingsession', 'session_id', f'user_id={pre_checkout_query.from_user.id} AND status!=3')[0][0]
    db.delete('accounts_cartitem', f'session_id={session_id}')