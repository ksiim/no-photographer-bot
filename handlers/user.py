from aiogram import F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, CallbackQuery, FSInputFile
)

from bot import dp, bot

from models.dbs.orm import Orm
from models.dbs.models import *

from .callbacks import *
from .markups import *
from .states import *

@dp.message(Command('start'))
async def start_message_handler(message: Message, state: FSMContext):
    await state.clear()
    
    if await Orm.get_user_by_telegram_id(message.from_user.id) is not None:
        return await message.answer(
            text=start_new_session_text,
            reply_markup=start_new_session_markup
        )
    await send_start_message(message)
    await state.set_state(UserStates.fio)

@dp.message(UserStates.fio)
async def get_person_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(UserStates.contact)
    await message.answer(
        text=contact_text,
        reply_markup=contact_markup
    )
    
@dp.message(UserStates.contact, F.contact)
async def get_person_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    await Orm.create_user(
        message=message,
        fio=data['fio'],
        phone_number=message.contact.phone_number,
    )
    await message.answer(
        text=thanks_for_registration_text,
        reply_markup=start_new_session_markup
    )
    await state.clear()
    
@dp.callback_query(F.data == "start_new_session")
async def start_new_session(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await callback.message.answer(
        text=wait_for_approve_session_text
    )
    
    user = await Orm.get_user_by_telegram_id(callback.from_user.id)
    admin = await Orm.get_admin()
    await bot.send_message(
        chat_id=admin.telegram_id,
        text=f"Пользователь {user.fio} хочет начать новую сессию.",
        reply_markup=await generate_approve_session_markup(user.telegram_id)
    )

@dp.callback_query(PhotoCallback.filter())
async def send_original_photo(callback: CallbackQuery, callback_data: dict):
    await callback.message.delete_reply_markup()
    photo_id = callback_data.photo_id
    photo = await Orm.get_photo_by_id(photo_id)
    photo_path = await get_photo_path_by_filename(photo.photo_filename)
    
    await bot.send_document(
        chat_id=callback.from_user.id,
        document=FSInputFile(photo_path),
    )
