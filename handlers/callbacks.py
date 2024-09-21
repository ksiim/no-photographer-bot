from aiogram.filters.callback_data import CallbackData

class SessionCallback(CallbackData, prefix="session"):
    user_id: int
    action: str
    
class PhotoCallback(CallbackData, prefix="photo"):
    photo_id: int