from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from filters.chat_types import ChatTypeFilter
from helpers.replies_texts import ABOUT_BOT_ENG, HELP_ENG, GREETING_ENG
from keyboards import reply
from keyboards.reply import MyCallback
from handlers.flight_handlers import my_flight_router
from requests_to_api.get_server_status import check_server_status

my_user_private = Router()
my_user_private.message.filter(ChatTypeFilter(['private']))
my_user_private.include_routers(my_flight_router)


@my_user_private.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    res = check_server_status()
    if res.get('status'):
        await state.clear()
        await message.answer(GREETING_ENG, reply_markup=reply.start_kb, parse_mode='Markdown')
    else:
        await message.answer("❌ A server error occurred. Please try again later. /start")


@my_user_private.callback_query(MyCallback.filter(F.foo == "favorites"))
async def favorites_cmd(query: types.CallbackQuery):
    await query.message.answer("Here is your list of favorite flights.")


@my_user_private.callback_query(MyCallback.filter(F.foo == "track"))
async def track_cmd(query: types.CallbackQuery):
    await query.message.answer("Enter the flight information you want to add to favorites.")


@my_user_private.callback_query(MyCallback.filter(F.foo == "untrack"))
async def untrack_cmd(query: types.CallbackQuery):
    await query.message.answer("Enter the flight information you want to remove from favorites.")


@my_user_private.callback_query(MyCallback.filter(F.foo == "notifications"))
async def notifications_cmd(query: types.CallbackQuery):
    await query.message.answer("Set up price drop or rise notifications.")


@my_user_private.callback_query(MyCallback.filter(F.foo == "settings"))
async def settings_cmd(query: types.CallbackQuery):
    await query.message.answer("Bot settings.")


@my_user_private.callback_query(MyCallback.filter(F.foo == "about"))
async def about_cmd(query: types.CallbackQuery):
    await query.message.answer(ABOUT_BOT_ENG)


@my_user_private.callback_query(MyCallback.filter(F.foo == "help"))
async def help_cmd(query: types.CallbackQuery):
    await query.message.answer(HELP_ENG, parse_mode="Markdown")
