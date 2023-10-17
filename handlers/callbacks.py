from aiogram.filters.callback_data import CallbackData


class GetSubscribeCallback(CallbackData, prefix='get_subscribe'):
    amount: int
    
class CheckPaymentCallback(CallbackData, prefix='check_payment'):
    amount: int
    fio: str
    
class ConfirmPaymentCallback(CallbackData, prefix='confirm_payment'):
    amount: int
    fio: str
    telegram_id: int