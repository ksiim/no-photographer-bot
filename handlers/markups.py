import os
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from bot import bot
from config import directory

from .callbacks import *

async def generate_raw_photo_markup(photo_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Получить оригинал",
                    callback_data=PhotoCallback(photo_id=photo_id).pack()
                )
            ]
        ]
    )
    
async def generate_extend_session_markup(user_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Продлить на 30 минут",
                    callback_data=ExtendSessionCallback(user_id=user_id, action="extend", extend_time=30).pack()
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Продлить на 60 минут",
                    callback_data=ExtendSessionCallback(user_id=user_id, action="extend", extend_time=60).pack()
                )
            ]
        ]
    )
    return keyboard

async def generate_extend_session_for_admin_markup(user_id, extend_time):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить",
                    callback_data=ExtendSessionAdminCallback(user_id=user_id, action="approve", extend_time=extend_time).pack()
                ),
                InlineKeyboardButton(
                    text="Отклонить",
                    callback_data=ExtendSessionAdminCallback(user_id=user_id, action="decline", extend_time=extend_time).pack()
                )
            ]
        ]
    )
    return keyboard

async def generate_end_session_timer_text(session):
    time_of_session_in_minutes = (session.end_time - session.start_time).seconds // 60
    return f"\nСессия длилась {time_of_session_in_minutes} минут."
    
async def get_photo_path_by_filename(filename):
    return os.path.join(directory, filename)
    
async def get_opened_photo_by_filename(filename):
    photo_path = await get_photo_path_by_filename(filename)
    return open(photo_path, "rb")

async def generate_start_text(message):
    return f"Привет, {message.from_user.full_name}! Я - бот, который поможет тебе воспользоваться нашей фото-студией без фотографа. Напиши мне свое ФИО в формате Фамилия Имя Отчество, например: Иванов Иван Иванович"

async def send_start_message(message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text=await generate_start_text(message=message)
    )
    
async def generate_approve_session_markup(user_telegram_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить",
                    callback_data=SessionCallback(user_id=user_telegram_id, action="approve").pack()
                ),
                InlineKeyboardButton(
                    text="Отклонить",
                    callback_data=SessionCallback(user_id=user_telegram_id, action="decline").pack()
                )
            ]
        ]
    )
    
async def generate_extending_text(user_fio, extend_time):

    return f"Пользователь {user_fio} хочет продлить сессию на {extend_time} минут."

async def generate_session_time_ended_text_for_admin(user_fio):
    return f"Сессия пользователя {user_fio} завершена по истечении времени."

contact_text = "Теперь поделись своим контактом, чтобы я мог идентифицировать тебя в нашей базе данных."
start_new_session_text = "Начнем новую сессию?"
thanks_for_registration_text = "Спасибо! Теперь ты можешь начать новую сессию."
session_time_ended_text = "Время сессии закончилось. Хочешь продлить ее?"
wait_for_approve_session_text = "Ожидайте подтверждения сессии от администратора."
session_approved_text = "\n\nНачало сессии подтверждено."
session_declined_text = "\n\nНачало сессии отклонено."
session_handled_ended_text = "\n\nСессия принудительно завершена."
end_session_one_hour_text = "\n\nСессия завершена по истечении часа."
session_extend_text = "Ваша сессия закончится через ~10 минут. Хотите продлить сессию?"

start_new_session_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Начать новую сессию",
                callback_data="start_new_session"
            ),
        ]
    ]
)

session_end_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Завершить сессию",
                callback_data="end_session"
            )
        ]
    ]
)

contact_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="☎️Поделиться контактом", request_contact=True)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)