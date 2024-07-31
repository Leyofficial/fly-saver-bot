from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv
from os import getenv
import asyncio
from handlers.user_private import my_user_private
load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message', 'edited_message']

dp = Dispatcher()
bot = Bot(token=getenv('TOKEN'))

dp.include_routers(my_user_private)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
