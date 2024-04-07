from aiogram import types
from aiogram.dispatcher import FSMContext
from asyncio import sleep
from datetime import datetime

from loader import dp, db
from keyboards.default.btns import send_phone_btn
from keyboards.inline.cartKeyboard import pay_type_btns, buy_btns
from keyboards.inline.subKeyboard import sub_keyboard
from keyboards.inline.prKeyboard import pr_keyboard
from keyboards.inline.detailKeyboard import detail_keyboard, next_add
from keyboards.default.mainKeyboard import main_keyboard
from states.buyStates import BuytState


@dp.callback_query_handler(text='cancel-call', state='*')
async def sup_cancel_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer('✅ Bekor qilindi!')
    await call.message.answer('Asosiy menyu', reply_markup=main_keyboard())
    await call.message.delete()
    await state.finish()



@dp.callback_query_handler(text='shopping_cart')
async def cart_handler(call: types.CallbackQuery):
    db.select('accounts_shoppingsession', 'session_id', f'user_id={call.from_user.id}')
    await call.answer("Savat bo'sh")


@dp.callback_query_handler(text_contains='pr_count=')
async def cart_handler(call: types.CallbackQuery):
    await call.answer(f'🛍 Savatda bu mahsulotdan {call.data[9:]} dona')


@dp.callback_query_handler(text_contains='buy_pr:')
async def session_handler(call: types.CallbackQuery):
    user = call.from_user
    # pr_title = call.message.text[:call.message.entities[0].length]
    pr_title = call.data[7:]
    product_id = db.select('products_product', 'id', where=f'title="{pr_title}"')[0][0]

    session = db.select('accounts_shoppingsession', 'session_id, status', where=f'user_id={user.id} AND status !=3')

    if not session:     # agar session bo'lmasa yoki payed bolsa yangi session ochamiz
        db.insert('accounts_shoppingsession', None, user.id, 1, 0, datetime.now())

    session = db.select('accounts_shoppingsession', 'session_id, status', where=f'user_id={user.id} AND status !=3')
    session_id, session_status = session[0]
    is_already = db.select('accounts_cartitem', 'id, quantity', where=f'session_id={session_id} AND product_id={product_id}')

    if not is_already:
        db.insert('accounts_cartitem', None, 0, datetime.now(), product_id, session_id)

    id_in_cart, product_quantity = db.select('accounts_cartitem', 'id, quantity', where=f'session_id={session_id} AND product_id={product_id}')[0]
    new_quantity = product_quantity + 1
    db.update('accounts_cartitem', f'id = {id_in_cart}', quantity=new_quantity)
    sub_name = call.message.reply_markup.inline_keyboard[1][0].callback_data
    await call.message.edit_reply_markup(reply_markup=next_add(next_count=new_quantity, subctg_name=sub_name))


    await call.answer(f"✅ Savatga qo'shildi. Bu mahsulot savatda {new_quantity} dona")
    # sub_name = call.message.reply_markup.inline_keyboard[1][0].callback_data
    # await call.message.edit_reply_markup(reply_markup=next_add(subctg_name=sub_name))


@dp.callback_query_handler(text_contains='_again')
async def again_handler(call: types.CallbackQuery):
    try:
        pr_title = call.message.text[:call.message.entities[0].length]
        quantity = int(call.message.reply_markup.inline_keyboard[0][1].callback_data[9:])
        # print(quantity)
        # return

        sub_name = call.message.reply_markup.inline_keyboard[1][0].callback_data
        product_id = db.select('products_product', 'id', where=f'title="{pr_title}"')[0][0]
        session = db.select('accounts_shoppingsession', 'session_id', where=f'user_id={call.from_user.id} AND status !=3')
        session_id = session[0][0]
        id_in_cart = db.select('accounts_cartitem', 'id', where=f'session_id={session_id} AND product_id={product_id}')[0][0]
        new_quantity = None
        if call.data[:3] == 'add':
            new_quantity = quantity + 1
        elif call.data[:3] == 'del':
            new_quantity = quantity - 1
            if quantity == 1:
                await call.message.edit_reply_markup(reply_markup=detail_keyboard(pr_title, sub_name))
                db.delete('accounts_cartitem', f'id = {id_in_cart}')
                return
        db.update('accounts_cartitem', f'id = {id_in_cart}', quantity=new_quantity)
        await call.message.edit_reply_markup(reply_markup=next_add(new_quantity, sub_name))
        await call.answer(f"✅ Savatga qo'shildi. Endi savatda {new_quantity} dona")
    except Exception as err:
        await call.message.answer(err)


@dp.callback_query_handler(text='main-menu')
async def main_menu_handler(call: types.CallbackQuery):
    await call.message.edit_text('🏠')
    await dp.bot.send_message(call.from_user.id, text='Asosiy menu', reply_markup=main_keyboard())
    await sleep(2.5)
    await call.message.delete()

@dp.callback_query_handler(text='back_to_type_pay', state='*')
async def cancel_pay(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="<b>To'lov turini tanlang:</b>", reply_markup=buy_btns)
    await state.finish()

@dp.callback_query_handler(text='buy-type-from-shop')
async def from_shop_handler(call: types.CallbackQuery):
    await call.message.answer('Buyurtmani rasmiylashtirish uchun telefon raqamingizni yuboring.', reply_markup=send_phone_btn)
    await call.message.delete()
    await BuytState.waiting_phone.set()


@dp.callback_query_handler()
async def main_query_handler(call: types.CallbackQuery):
    if db.select('products_category', where=f'name="{call.data}"'):         # is category
        ctg_id = db.select('products_category', 'id', f'name="{call.data}"')[0][0]
        await call.message.edit_text('Kategoriyani tanlang:', reply_markup=sub_keyboard(ctg_id))

    elif db.select('products_subcategory', where=f'name="{call.data}"'):    # is subcategory name
        try:
            sub_name = call.data
            sub_id = db.select('products_subcategory', 'id', f'name="{sub_name}"')[0][0]
            ctg_id = db.select('products_subcategory', 'category_id', f'name="{sub_name}"')[0][0]
            ctg = db.select('products_category', 'name', f'id={ctg_id}')[0][0]

            products = db.select('products_product', 'title', f'subcategory_id = {sub_id}')
            await call.message.edit_text('Mahsulotni tanlang:', reply_markup=pr_keyboard(products, ctg))

        except:
            pass

    elif db.select('products_product', where=f'title="{call.data}"'):       # is product title
        pr_id, pr_title, pr_desc, pr_price, pr_image,subctg_id = \
            db.select('products_product', 'id, title, description, price, image, subcategory_id', f'title="{call.data}"')[0]
        subctg_name = db.select('products_subcategory', 'name', f'id={subctg_id}')[0][0]


        session = db.select('accounts_shoppingsession', 'session_id, status', where=f'user_id={call.from_user.id} AND status !=3')

        if not session:
            db.insert('accounts_shoppingsession', None, call.from_user.id, 1, 0, datetime.now())
            session = db.select('accounts_shoppingsession', 'session_id, status', where=f'user_id={call.from_user.id} AND status !=3')

        session_id = session[0][0]
        is_already = db.select('accounts_cartitem', 'quantity', where=f'session_id={session_id} AND product_id={pr_id}')

        txt = f"<b>{pr_title}</b> <a href='{pr_image}'> </a>\n\n{pr_desc}\n\n<b>👉 Narxi: {pr_price} so'm</b>"

        if is_already:
            quantity = is_already[0][0]
            await call.message.edit_text(txt, reply_markup=next_add(next_count=quantity, subctg_name=subctg_name))
            return

        await call.message.edit_text(txt, reply_markup=detail_keyboard(pr_title, subctg_name))

