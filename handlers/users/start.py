from aiogram import types
from aiogram.dispatcher import FSMContext
from asyncio import sleep


from loader import dp, db
from keyboards.default.mainKeyboard import main_keyboard


@dp.message_handler(commands=['start'], state='*')
async def bot_start(msg: types.Message, state: FSMContext):
    user = msg.from_user
    db.add_user(user.id, user.first_name, user.last_name, user.username)
    await msg.answer('🎊')
    await msg.answer(f"Salom, {user.full_name}!", reply_markup=main_keyboard())
    await sleep(3)
    await dp.bot.delete_message(msg.chat.id, msg.message_id+1)

    await state.finish()

