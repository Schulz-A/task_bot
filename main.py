import asyncio
import betterlogging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from nowpayments.sandbox import NOWPaymentsSandbox

from tg_bot.config import get_config
from tg_bot.dialogs.setup_dialogs import register_all_dialogs
from tg_bot.handlers.additem import add_item
from tg_bot.handlers.adminshandlers import admin_router
from tg_bot.handlers.buy import buy_router
from tg_bot.handlers.cart_handlers import cart_router
from tg_bot.handlers.feedback import feedback_router
from tg_bot.handlers.items import items_router
from tg_bot.handlers.itemspreview import item_router
from tg_bot.handlers.mailing import mailing_router
from tg_bot.handlers.referralsys import referral_router
from tg_bot.handlers.starthandlers import start_router
from tg_bot.handlers.users import users_router
from tg_bot.infrastructure.database.functions.setupdb import create_session_pool
from tg_bot.middlewares.databasemiddleware import DataBaseMiddleWare
from tg_bot.middlewares.quaryanswermiddleware import CBQAnswerMiddleware

betterlogging.basic_colorized_config(level='INFO')


def register_all_middlewares(dp: Dispatcher, session_pool):
    dp.message.outer_middleware(DataBaseMiddleWare(session_pool))
    dp.callback_query.outer_middleware(DataBaseMiddleWare(session_pool))
    dp.inline_query.outer_middleware(DataBaseMiddleWare(session_pool))
    dp.callback_query.middleware(CBQAnswerMiddleware())


async def main():
    config = get_config('.env')
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    storage = RedisStorage.from_url(config.redis_config.dsn(), key_builder=DefaultKeyBuilder(with_destiny=True))

    payment = NOWPaymentsSandbox(config.miscellaneous.wallet_key)

    dp = Dispatcher(storage=storage, config=config, payment=payment)
    session_pool = await create_session_pool(config.db_config)
    routers = [
        start_router,
        admin_router,
        add_item,
        item_router,
        cart_router,
        buy_router,
        referral_router,
        feedback_router,
        mailing_router,
        users_router,
        items_router
    ]
    dp.include_routers(*routers)
    register_all_middlewares(dp, session_pool)
    register_all_dialogs(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemError):
        betterlogging.error('Bot stopped!!!')
