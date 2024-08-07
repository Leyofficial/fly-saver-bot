import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram import types
from dotenv import find_dotenv, load_dotenv

from handlers.chat_procedure import my_chat_procedure
from handlers.group_chat import my_group_chat
from handlers.user_private import my_user_private
from helpers.bot_cmds_list import private

load_dotenv(find_dotenv())
bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot=bot)

dp.include_routers(my_user_private, my_group_chat, my_chat_procedure)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


asyncio.run(main())
