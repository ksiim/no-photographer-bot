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

import datetime

CHANNEL_ID = -1001980386639


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

@dp.message(F.text == '🧘‍♀️Обо мне')
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
    
@dp.message(F.text == '🤍Подписка')
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
    
@dp.callback_query(GetSubscribeCallback.filter())
async def get_subscribe_callback(callback: CallbackQuery,
                                 callback_data: CallbackData,
                                 state: FSMContext):
    amount = callback_data.amount
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
        text=f'Теперь переведи {amount}P на счёт\n<code>2200700449365633</code>\n+<code>79959182053</code> Тинькофф\nПолучатель: Беккер Даниил Юрьевич',
        reply_markup=await generate_check_payment_keyboard(amount=amount,
                                                           fio=fio)
    )
    
@dp.message(F.text == '☎️Связь со мной')
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
    await callback.message.answer(
        text='Осталось дождаться подтверждения перевода. Я добавлю тебя в чат, когда администратор подвердит оплату'
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