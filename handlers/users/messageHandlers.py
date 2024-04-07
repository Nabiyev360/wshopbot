from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from keyboards.inline.subKeyboard import sub_keyboard
from keyboards.inline.supportKeyboards import support_keyboard
from keyboards.inline.cartKeyboard import buy_btns, pay_type_btns
from keyboards.default.mainKeyboard import main_keyboard
from states.supportState import SupportState
from states.buyStates import BuytState
from data.config import ADMINS


@dp.message_handler(text='📲 Murojaat uchun')
async def support_handler(msg: types.Message, state: FSMContext):
    await msg.answer(
        text="Biz sizning ixtiyoriy sovolingizga javob berishdan xursandmiz. \nMarhamat, xabaringizni jo'natishingiz mumkin.",
        reply_markup=support_keyboard
    )

    await SupportState.waiting_message.set()


@dp.message_handler(state=SupportState.waiting_message, content_types=types.ContentType.ANY)
async def base_msg_handler(msg: types.Message, state: FSMContext):
    await msg.forward(ADMINS[0])
    await msg.reply("✅ Xabar adminga yuborildi, tez orada javob qaytaramiz!", reply_markup=main_keyboard())
    await state.finish()
    await dp.bot.delete_message(msg.chat.id, msg.message_id-1)
    await dp.bot.delete_message(msg.chat.id, msg.message_id-2)


@dp.message_handler(state=BuytState.waiting_location)
async def location_handler(msg: types.Message, state: FSMContext):
    await state.update_data(
        {f'location_{msg.from_user.id}':msg.text}
    )
    await msg.answer("<b>To'lov turini tanlang:</b>", reply_markup=pay_type_btns)
    await state.finish()


@dp.message_handler(content_types=types.ContentType.ANY, state=BuytState.waiting_phone)
async def phone_handler(msg: types.Message, state: FSMContext):
    await msg.answer(
        text="✅ Buyurtmangiz uchun raxmat, tez orada operatorlarimiz siz bilan bog'lanadi",
        reply_markup=main_keyboard()
    )
    session_id = db.select('accounts_shoppingsession', 'session_id', f'user_id={msg.from_user.id} AND status!=3')[0][0]
    db.delete('accounts_cartitem', f'session_id={session_id}')
    await state.finish()



@dp.message_handler()
async def base_msg_handler(msg: types.Message):
    if db.select('products_category', where=f'name="{msg.text}"'):
        ctg_id = db.select('products_category', 'id', f'name="{msg.text}"')[0][0]
        await msg.answer('Kategoriyani tanlang:', reply_markup=sub_keyboard(ctg_id))
