from bot import dp, bot

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message, CallbackQuery,
)
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram import F

from models.dbs.users import *
from models.dbs.message import *
from models.dbs.reviews import *

from .callbacks import *
from .markups import *
from .states import *

import datetime

CHANNEL_ID = -1001980386639


async def everyday_task():
    for user in User.get_all_users():
        try:
            member = await bot.get_chat_member(chat_id=CHANNEL_ID,
                                               user_id=user.telegram_id)
            if member.status.name != 'LEFT':
                if user.trialed:
                    if (datetime.datetime.now() - user.start_trial_date).days == 1:
                        await bot.send_message(chat_id=user.telegram_id,
                                            text='Твоя подписка закончилась😔\nПродолжить тренировки👇',
                                            reply_markup=subscribe_keyboard)
                        await kick_user(telegram_id=user.telegram_id)
                        return

                if (datetime.datetime.now() - user.finish_date).days == -3:
                    await bot.send_message(chat_id=user.telegram_id,
                                        text='Твоя подписка закончится через три дня. Продлить👇',
                                        reply_markup=subscribe_keyboard)
                    return
                if (datetime.datetime.now() - user.finish_date).days >= 0:
                    await bot.send_message(chat_id=user.telegram_id,
                                        text='Твоя подписка закончилась😔\nПродолжить тренировки👇',
                                        reply_markup=subscribe_keyboard)
                    await kick_user(telegram_id=user.telegram_id)
        except:
            pass
        
async def kick_user(telegram_id: int):
    await bot.ban_chat_member(chat_id=CHANNEL_ID,
                              user_id=telegram_id)
    await bot.unban_chat_member(chat_id=CHANNEL_ID,
                                user_id=telegram_id)


@dp.message(F.text == 'Закрыть')
@dp.message(Command('start'))
async def start_message(message: Message, state: FSMContext):
    if User.get_by_telegram_id(message.from_user.id) == None:
        user = User(telegram_id=message.from_user.id,
                    full_name=message.from_user.full_name,
                    username=message.from_user.username)
        user.save()
        
    start_text = f'''Привет, <b>{message.from_user.full_name}</b>
    
Меня зовут <b>Даниил</b>.
Я преподаю йогу по методологии FYSM в <b>закрытом телеграмм канале</b> «<i>САДХАКИ</i>».

Там есть практики в <b>записи и в прямом эфире</b>.

Вы можете <i>вступить в группу на 24 часа, в дальнейшем вы можете продолжить тренироваться по подписке.
Тренировки подходят как новичкам, так и продвинутым пользователям.</i>
'''
    await message.answer(
        text=start_text,
        reply_markup=start_keyboard
    )
    
@dp.callback_query(F.data == 'close')
async def close_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

@dp.message(F.text == '🧘🏻‍♂️Обо мне')
async def about_me(message: Message, state: FSMContext):
    await message.delete()
    
    photo = Messages.get_by_name(name='about_me_photo').info
    caption = '''Я преподаю йогу в стиле FYSM. Два года назад у меня были проблемы со спиной, желудком, моральным состоянием, и всего за один год практики, я избавился от всех хронических болячек и эмоциональной нестабильности за счет тренировок.
    
Я пришел в йогу не от хорошей жизни, но только йога смогла помочь мне по-настоящему.

За этот короткий срок я безопасно пришел к тем результатам, которые у меня есть:
— различные балансы на руках
— гибкость
— стабильное внутреннее состояние
и другие красивые асаны, которые вы можете увидеть в моем инстаграме.'''
    await bot.send_photo(photo=photo,
                         caption=caption,
                         chat_id=message.from_user.id,
                         reply_markup=close_keyboard)
    
@dp.message(F.text == '✍️Подписка')
async def subscribe_message(message: Message, state: FSMContext):
    subscribe_text = '''На канале безопасные практики, там нет лотосов и стоек на голове, но в то же время они за короткий срок построят мышечный корсет, подтянут ваше тело, разовьют гибкость.
        
-2 раза в неделю я провожу прямые эфиры, все записи сохраняются в группе.
-1 раз в месяц я провожу эфир на тематическую тему.
Так же в канале ты найдешь полезные лайфхаки, книги и много чего еще.

Можно начать заниматься, даже если у тебя нет опыта в йоге и ты считаешь себя не гибким человеком.

Всему можно научиться практикуя на канале и задавая вопросы.

Если у вас возникает вопрос по технике выполнения, можно прислать фото асан в комментарии под любой практикой или просто описать свои ощущения. Я на все отвечаю.

С каким запросом можно прийти?
— болит спина/ шея
— встать на руки
— хочется исправить осанку
— наладить контакт с телом (понимать свои желания, ощущения)
— построить мышечный корсет, подтянув тело
— улучшить растяжку, раскрыть грудной отдел, тазобедренные
— научиться контролировать дыхание в жизни/ во время стрессовых ситуаций
— поднять эмоциональный фон в плюс
— наладить режим сна

и много чего ещё.
'''
    await message.answer(
        text=subscribe_text,
        reply_markup=subscribe_keyboard
    )
    
async def get_media_reviews():
    media = MediaGroupBuilder()
    for review in Review.get_all_reviews():
        media.add_photo(media=review.photo)
    return media
    
@dp.message(F.text == '🗣️Отзывы')
async def reviews_message(message: Message, state: FSMContext):
    media = await get_media_reviews()
    await bot.send_media_group(chat_id=message.from_user.id,
                               media=media.build())
    await message.answer(
        text='Больше отзывов в моем инстаграме',
        reply_markup=subscribe_keyboard
    )

@dp.message(F.text =='👐Ответы на вопросы')
async def get_q_and_a(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(
        text='''Выбери вопрос, на который желаешь увидеть ответ''',
        reply_markup=q_and_a
    )
    
@dp.message(F.text == 'Какой уровень❓')
async def level(message: Message, state: FSMContext):
    await message.answer(
        text='Подойдёт новичкам и опытным практикующим.\nНа канале мы тренируем базу.'
    )
    
@dp.message(F.text == 'Как ориентироваться в канале❓')
async def orientir(message: Message, state: FSMContext):
    await message.answer(
        text='В канале есть хэштеги («руки», «растяжка», «кор», «балансы» и т.д.), чтобы вам было легко ориентироваться.\nА еще есть хэштег «эфир», по которому можно найти тематический эфир.\nВся важная информация находится в закрепе.'
    )

@dp.message(F.text == 'Длительность практик❓')
async def dlitelnost(message: Message, state: FSMContext):
    await message.answer(
        text='Занятия идут от 20 минут, до 1:30. \nВы можете заниматься по разным практикам каждый день, можете 2 раза в неделю. Можете в записи, можете в прямом эфире.'
    )
    
@dp.message(F.text == 'Что мне нужно для практики❓')
async def mesto(message: Message):
    await message.answer(
        text='Место 2х2 метра и коврик.'
    )
    
@dp.message(F.text == 'Сколько стоит❓')
async def howmuchforthis(message: Message):
    await message.answer(
        text='1500₽ на целый месяц с доступом ко всем практикам и прямым эфирам, так же есть тариф на 3 месяца – 3000р'
    )
    
@dp.callback_query(GetSubscribeCallback.filter())
async def get_subscribe_callback(callback: CallbackQuery,
                                 callback_data: CallbackData,
                                 state: FSMContext):
    amount = callback_data.amount
    await callback.message.delete_reply_markup()
    if amount == 0:
        await trial_period(callback=callback)
        return
    await state.update_data(amount=amount)
    await callback.message.answer(
        text='Для того, чтобы я мог определить, кто мне перевел деньги, мне нужно знать твое имя и твою фамилию.\n\nОтправь мне их, например: Иванов Иван'
    )
    await state.set_state(PaymentState.get_fio)
    
@dp.message(PaymentState.get_fio)
async def get_fio_for_payment(message: Message, state: FSMContext):
    if len(message.text.split()) != 2:
        await message.answer(
            text='Ты отправил фамилию и имя не как в примере. Попробуй снова\n\nПример: Иванов Иван'
        )
        return
    data = await state.get_data()
    amount = data["amount"]
    fio = message.text
    await message.answer(
        text=f'Реквизиты для перевода\n<code>2200700449365633</code>\n+<code>79959182053</code> Тинькофф\nПолучатель: Беккер Даниил Юрьевич\n\nСумма: {amount}',
        reply_markup=await generate_check_payment_keyboard(amount=amount,
                                                           fio=fio)
    )
    
@dp.message(F.text == '🤝Связь со мной')
async def message_to_me(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(
        text='@bekkerdanya - можешь написать мне в личные сообщения',
        reply_markup=close_keyboard
    )    

async def trial_period(callback: CallbackQuery):
    user = User.get_by_telegram_id(callback.from_user.id)
    if user.trialed:
        await callback.answer(
            text='Ты уже использовал пробный период'
        )
        return
    link = await bot.create_chat_invite_link(
        chat_id=CHANNEL_ID,
        member_limit=1
    )
    link = link.invite_link
    user.start_trial_date = datetime.datetime.now()
    user.trialed = True
    user.save()
    await callback.message.answer(
        text='Присоединяйся к моему каналу на день!',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Присоединиться', url=link)]
            ]
        )
    )
    
@dp.callback_query(CheckPaymentCallback.filter())
async def check_payment_callback(
    callback: CallbackQuery,
    callback_data: CallbackData,
    state: FSMContext
):
    await callback.message.delete_reply_markup()
    await callback.message.answer(
        text='В течение 12 часов администатор подтвердит оплату и я добавлю тебя в чат!'
    )
    fio = callback_data.fio
    await state.clear()
    amount = callback_data.amount
    telegram_id = callback.from_user.id
    admin_id = User.get_admins()[-1].telegram_id
    await bot.send_message(
        chat_id=admin_id,
        text=f"{fio} должен(-на) был(-а) перевести {amount}Р",
        reply_markup=await generate_confirm_payment_keyboard(
            amount=amount,
            fio=fio,
            telegram_id=telegram_id
        )
    )
    
# @dp.message(Command('ban'))
# async def ban(message: Message, state: FSMContext):
#     await bot.ban_chat_member(chat_id=CHANNEL_ID,
#                               user_id=message.from_user.id)
#     await bot.unban_chat_member(chat_id=CHANNEL_ID,
#                                 user_id=message.from_user.id)
        
# @dp.message(F.text)
# async def aaa(message: Message, state: FSMContext):
#     await bot.send_message(chat_id=message.from_user.id,
#                            text=str(message.forward_from_chat.id))

# @dp.message(F.photo)
# async def photo_id(message: Message, state: FSMContext):
#     await message.answer(
#         text=f'<code>{message.photo[-1].file_id}</code>'
#     )