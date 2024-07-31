from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, or_f
from filters.chat_types import ChatTypeFilter
from common.replies_texts import ABOUT_BOT, GREETING, HELP
from keyboards import reply

my_user_private = Router()
my_user_private.message.filter(ChatTypeFilter(['private']))


@my_user_private.message(or_f(CommandStart(), F.text.lower().contains('запуск')))
async def start_cmd(message: types.Message):
    await message.answer(GREETING, reply_markup=reply.start_kb)


@my_user_private.message(or_f(Command('about'), F.text.lower().contains('о нас')))
async def about_cmd(message: types.Message):
    await message.answer(ABOUT_BOT)


@my_user_private.message(or_f(Command('help'), F.text.lower().contains('помощь')))
async def help_cmd(message: types.Message):
    await message.answer(HELP)


@my_user_private.message(or_f(Command('search'), F.text.lower().contains('поиск')))
async def search_cmd(message: types.Message):
    await message.answer("Введите город отправления, пункт назначения и даты поездки для поиска билетов.")


@my_user_private.message(or_f(Command('favorites'), F.text.lower().contains('избранные')))
async def favorites_cmd(message: types.Message):
    await message.answer("Вот список ваших избранных рейсов.")


@my_user_private.message(or_f(Command('track'), F.text.lower().contains('добавить')))
async def track_cmd(message: types.Message):
    await message.answer("Введите информацию о рейсе, который хотите добавить в избранное.")


@my_user_private.message(or_f(Command('untrack'), F.text.lower().contains('удалить')))
async def untrack_cmd(message: types.Message):
    await message.answer("Введите информацию о рейсе, который хотите удалить из избранного.")


@my_user_private.message(or_f(Command('notifications'), F.text.lower().contains('уведомления')))
async def notifications_cmd(message: types.Message):
    await message.answer("Настройте уведомления о снижении или повышении цен.")


@my_user_private.message(or_f(Command('settings'), F.text.lower().contains('настройки')))
async def settings_cmd(message: types.Message):
    await message.answer("Настройки бота.")


# @my_user_private.message(F.contact)
# async def get_contact(message: types.Message):
#     await message.answer(f"Номер получена")
#     await message.answer(str(message.contact))
#
#
# @my_user_private.message(F.location)
# async def get_location(message: types.Message):
#     await message.answer(f"Локация получена")
#     await message.answer(str(message.location))
