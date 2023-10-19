from aiogram.filters.callback_data import CallbackData


class GetSubscribeCallback(CallbackData, prefix='getSubs'):
    amount: int
    
class CheckPaymentCallback(CallbackData, prefix='checkPay'):
    amount: int
    fio: str
    
class ConfirmPaymentCallback(CallbackData, prefix='pay'):
    amount: int
    fio: str
    telegram_id: int
    
class ReviewCallback(CallbackData, prefix='review'):
    operation: str
    
class DeleteReviewCallback(CallbackData, prefix='delRev'):
    name: str