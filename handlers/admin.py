from bot import dp, bot

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

from models.dbs.models import *

from .callbacks import *
from .markups import *
from .states import *

from .user import *

@dp.callback_query(SessionCallback.filter())
async def approve_or_decline_session(callback: CallbackQuery, callback_data: dict):
    await callback.message.delete_reply_markup()
    user = await Orm.get_user_by_telegram_id(callback_data.user_id)
    reply_markup = None
    if callback_data.action == "approve":
        await Orm.start_new_session(user)
        session_text = session_approved_text
        reply_markup = session_end_markup
    elif callback_data.action == "decline":
        session_text = session_declined_text
    await edit_text_with_session_action(callback, session_text, reply_markup=reply_markup)
    
    await bot.send_message(
        chat_id=user.telegram_id,
        text=session_text
    )
    
@dp.callback_query(ExtendSessionAdminCallback.filter())
async def extend_session_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    action = callback.data.split(":")[2]
    user_id = int(callback.data.split(":")[1])
    extend_time = int(callback.data.split(":")[3])
    user = await Orm.get_user_by_telegram_id(user_id)
    if action == "approve":
        await Orm.extend_session(user_id, extend_time)
        text = f"Сессия продлена на {extend_time} минут"
    elif action == "decline":
        text = "Продление сессии отклонено"
    await edit_text_with_session_action(callback, text, reply_markup=session_end_markup)
    await bot.send_message(
        chat_id=user.telegram_id,
        text=text
    )

async def edit_text_with_session_action(callback, text, reply_markup=None):
    await callback.message.edit_text(
            text=callback.message.text + text,
            reply_markup=reply_markup
        )
    
@dp.callback_query(F.data == "end_session")
async def end_session(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    user = await Orm.end_session()
    timer_text = await generate_end_session_timer_text(session=await Orm.get_last_session_by_telegram_id(user.telegram_id))
    await callback.message.edit_text(
        text=callback.message.text + session_handled_ended_text + timer_text,
    )
    await bot.send_message(
        chat_id=user.telegram_id,
        text=session_handled_ended_text + timer_text,
        reply_markup=start_new_session_markup
    )