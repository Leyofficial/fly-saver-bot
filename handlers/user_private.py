from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from filters.chat_types import ChatTypeFilter
from helpers.replies_texts import ABOUT_BOT, GREETING, HELP
from keyboards import reply
from keyboards.reply import MyCallback, lang_kb
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
        await message.answer(_(GREETING))
        await message.answer(_("🌐 Пожалуйста, выберите язык, который вы хотите использовать:"), reply_markup=lang_kb)
        # await message.answer(GREETING, reply_markup=reply.start_kb, parse_mode='Markdown')
    else:
        await message.answer(_("❌ Произошла ошибка на сервера. Пожалуйста, попробуйте позже. /start"))


@my_user_private.callback_query(MyCallback.filter(F.foo == "favorites"))
async def favorites_cmd(query: types.CallbackQuery):
    await query.message.answer(_("Вот список ваших избранных рейсов."))


@my_user_private.callback_query(MyCallback.filter(F.foo == "track"))
async def track_cmd(query: types.CallbackQuery):
    await query.message.answer(_("Введите информацию о рейсе, который хотите добавить в избранное."))


@my_user_private.callback_query(MyCallback.filter(F.foo == "untrack"))
async def untrack_cmd(query: types.CallbackQuery):
    await query.message.answer(_("Введите информацию о рейсе, который хотите удалить из избранного."))


@my_user_private.callback_query(MyCallback.filter(F.foo == "notifications"))
async def notifications_cmd(query: types.CallbackQuery):
    await query.message.answer(_("Настройте уведомления о снижении или повышении цен."))


@my_user_private.callback_query(MyCallback.filter(F.foo == "settings"))
async def settings_cmd(query: types.CallbackQuery):
    await query.message.answer(_("Настройки бота."))


@my_user_private.callback_query(MyCallback.filter(F.foo == "about"))
async def about_cmd(query: types.CallbackQuery):
    await query.message.answer(ABOUT_BOT)


@my_user_private.callback_query(MyCallback.filter(F.foo == "help"))
async def help_cmd(query: types.CallbackQuery):
    await query.message.answer(HELP)


@my_user_private.callback_query(MyCallback.filter(F.foo.in_({"en", "ru", "es"})))
async def set_language(query: types.CallbackQuery, callback_data: MyCallback, state: FSMContext):
    lang = callback_data.foo
    await state.update_data(language=lang)
    await query.message.answer(_("Язык успешно изменен!"), reply_markup=reply.start_kb)