from aiogram.filters.callback_data import CallbackData

class SessionCallback(CallbackData, prefix="session"):
    user_id: int
    action: str
    
class ExtendSessionCallback(CallbackData, prefix="extend_session"):
    user_id: int
    action: str
    extend_time: int
    
class PhotoCallback(CallbackData, prefix="photo"):
    photo_id: int
    
class ExtendSessionAdminCallback(CallbackData, prefix="extend_session_admin"):
    user_id: int
    action: str
    extend_time: int