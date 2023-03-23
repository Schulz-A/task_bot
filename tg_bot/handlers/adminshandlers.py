from aiogram import Router, F, types, Bot

from tg_bot.config import Config
from tg_bot.keyboards.startkeyboard import admin_keyboard

admin_router = Router()


@admin_router.callback_query(F.data == "admin_panel")
async def admin_panel(call: types.CallbackQuery, config: Config, bot: Bot):
    user_id = int(call.from_user.id)
    if user_id not in config.tg_bot.admins:
        await call.answer("Вы не являетесь администратором")
        return
    
    await call.message.edit_text("🎛 Панель администратора", reply_markup=admin_keyboard)