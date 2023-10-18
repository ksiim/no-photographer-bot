from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from bot import bot

from .callbacks import *

from models.dbs.reviews import *


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🧘‍♀️Обо мне'), KeyboardButton(text='🤍Подписка')],
        [KeyboardButton(text='💫Отзывы'), KeyboardButton(text='👐Ответы на вопросы')],
        [KeyboardButton(text='☎️Связь со мной')],
    ],
    resize_keyboard=True
)

subscribe_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Оформить подписку на месяц Цена 1490Р',
                              callback_data=GetSubscribeCallback(amount=1490).pack())],
        [InlineKeyboardButton(text='Оформить подписку на 3 месяца Цена 3000Р',
                              callback_data=GetSubscribeCallback(amount=3000).pack())],
        [InlineKeyboardButton(text='Вступить в группу на 24 часа бесплатно',
                              callback_data=GetSubscribeCallback(amount=0).pack())],
    ]
)

async def generate_check_payment_keyboard(amount, fio):
    check_payment_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Проверить оплату', callback_data=CheckPaymentCallback(amount=amount,
                                                                                              fio=fio).pack())]
        ]
    )
    return check_payment_keyboard

async def generate_confirm_payment_keyboard(amount, fio, telegram_id):
    confirm_payment_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Подтвердить перевод',
                                  callback_data=ConfirmPaymentCallback(
                amount=amount, fio=fio, telegram_id=telegram_id
            ).pack())]
        ]
    )
    return confirm_payment_keyboard

async def generate_delete_review_keyboard():
    reviews = Review.get_all_reviews()
    buttons = []
    for review in reviews:
        buttons.append([InlineKeyboardButton(
            text=review.name,
            callback_data=DeleteReviewCallback(name=review.name).pack()
        )])
    delete_review_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[buttons]
    )
    return delete_review_keyboard

close_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Закрыть', callback_data='close')]
    ]
)

admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Изменить фото "Обо мне"', callback_data='change-about-photo')],
        [InlineKeyboardButton(text='Удалить отзыв', callback_data=ReviewCallback(
            operation='delete').pack()),
         InlineKeyboardButton(text='Добавить отзыв', callback_data=ReviewCallback(
             operation='add'
         ).pack())]
    ]
)