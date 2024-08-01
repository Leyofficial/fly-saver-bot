from aiogram import Bot, Dispatcher, types
from dotenv import find_dotenv, load_dotenv
from os import getenv
import asyncio
from handlers.user_private import my_user_private
from handlers.chat_procedure import my_chat_procedure
from handlers.group_chat import my_group_chat
from common.bot_cmds_list import private

load_dotenv(find_dotenv())
# ALLOWED_UPDATES = ['message', 'edited_message', 'inline_buttons']

dp = Dispatcher()
bot = Bot(token=getenv('TOKEN'))

dp.include_routers(my_user_private, my_group_chat, my_chat_procedure)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


asyncio.run(main())
