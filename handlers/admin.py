from bot import dp, bot

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

from models.dbs.users import *
from models.dbs.message import Messages

from .callbacks import *
from .markups import *
from .states import *

from .user import *

import datetime


@dp.callback_query(ConfirmPaymentCallback.filter())
async def confirm_payment_callback(
    callback: CallbackQuery,
    callback_data: CallbackData,
    state: FSMContext
):
    await callback.message.delete_reply_markup()
    await callback.message.edit_text(text='ПОДТВЕРЖДЕН\n' + callback.message.text)
    telegram_id = callback_data.telegram_id
    amount = callback_data.amount
    if amount == 1490:
        days = 30
    if amount == 3000:
        days = 90
    finish_date = datetime.datetime.now() + datetime.timedelta(days=days)
    user = User.get_by_telegram_id(telegram_id=telegram_id)
    user.finish_date = finish_date
    user.save()
    
    link = await bot.create_chat_invite_link(chat_id=CHANNEL_ID,
                                             member_limit=1)
    link = link.invite_link
    await bot.send_message(chat_id=telegram_id,
                           text=f"Ты приобрел доступ к приватному каналу на {days} дней и твой перевод был подтвержден! Присоединяйся к каналу!!",
                           reply_markup=InlineKeyboardMarkup(
                               inline_keyboard=[
                                   [InlineKeyboardButton(text='Присоединиться', url=link)]
                               ]
                           ))
    

@dp.message(Command('admin'))
async def admin_message(message: Message, state: FSMContext):
    if not User.get_by_telegram_id(message.from_user.id).admin:
        return
    await message.answer(
        text='Привет, админ. Что будешь делать?',
        reply_markup=admin_keyboard
    )
    
@dp.callback_query(F.data == 'change-about-photo')
async def change_about_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text='Отправь новое фото, которое будет в графе "Обо мне"'
    )
    await state.set_state(ChangeState.about_me_photo)
    
@dp.message(ChangeState.about_me_photo, F.photo)
async def get_about_photo(message: Message, state: FSMContext):
    new_photo = message.photo[-1].file_id
    current_photo = Messages.get_by_name(name='about_me_photo')
    current_photo.info = new_photo
    current_photo.save()
    
    await message.answer(
        text='Фото было успешно изменено'
    )
    
    await state.clear()