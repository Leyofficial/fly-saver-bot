from typing import Any

from aiogram import Bot, Dispatcher, types
from aiogram.types import TelegramObject
from aiogram.utils.i18n import I18n
from dotenv import find_dotenv, load_dotenv
from os import getenv
import asyncio
from handlers.chat_procedure import my_chat_procedure
from handlers.group_chat import my_group_chat
from handlers.user_private import my_user_private
from helpers.bot_cmds_list import private
from middleware.i18n import SimpleI18nMiddleware, I18nMiddleware

i18n = I18n(path='../locales', default_locale="en", domain='messages')


class BotI18nMiddleware(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: dict[str, Any]) -> str:
        return 'en'


i18n_middleware = SimpleI18nMiddleware(i18n)

load_dotenv(find_dotenv())

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot=bot)
BotI18nMiddleware(i18n).setup(dp)

dp.include_routers(my_user_private, my_group_chat, my_chat_procedure)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


asyncio.run(main())
