from aiogram import Router, types
from aiogram.filters import CommandStart,Command

my_user_private = Router()

ABOUT_BOT = """
FlySaverBot ✈️

🔍 Ищи дешевые билеты: Введи город отправления, пункт назначения и даты поездки для поиска лучших предложений.

💼 Избранные рейсы: Сохраняй рейсы и отслеживай их цены.

📉 Уведомления о ценах: Получай оповещения о снижении и повышении цен на избранные рейсы.

Начни экономить на путешествиях с FlySaverBot!
"""


@my_user_private.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет, халявщик!")


@my_user_private.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer(ABOUT_BOT)

@my_user_private.message(Command('menu'))
async def menu_cmd(message: types.Message):
    await message.answer("Это меню!")

