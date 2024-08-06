from aiogram import Bot, Dispatcher, types
from dotenv import find_dotenv, load_dotenv
from os import getenv
import asyncio
from handlers.chat_procedure import my_chat_procedure
from handlers.group_chat import my_group_chat
from handlers.user_private import my_user_private
from helpers.bot_cmds_list import private
from middleware.db import CounterMiddleware

load_dotenv(find_dotenv())

dp = Dispatcher()
bot = Bot(token=getenv('TOKEN'))

my_user_private.message.middleware(CounterMiddleware())
dp.include_routers(my_user_private, my_group_chat, my_chat_procedure)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


asyncio.run(main())
