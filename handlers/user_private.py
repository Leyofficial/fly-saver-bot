from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from filters.chat_types import ChatTypeFilter
from common.replies_texts import ABOUT_BOT, GREETING, HELP
from keyboards import reply
from keyboards.reply import MyCallback

my_user_private = Router()
my_user_private.message.filter(ChatTypeFilter(['private']))


class AddFlight(StatesGroup):
    departure = State()
    arrival = State()
    departure_date = State()
    arrival_date = State()


@my_user_private.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(GREETING, reply_markup=reply.start_kb)


@my_user_private.callback_query(StateFilter(None), MyCallback.filter(F.foo == "search"))
async def departure_search_cmd(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer("Введите город отправления, пункт назначения и даты поездки для поиска билетов.")
    await query.message.answer("Откуда вы хотите полететь?")
    await state.set_state(AddFlight.departure)


@my_user_private.message(StateFilter(AddFlight.departure))
async def enter_departure(message: types.Message, state: FSMContext):
    await state.update_data(departure=message.text)
    await message.answer("Куда вы хотите полететь?")
    await state.set_state(AddFlight.arrival)


@my_user_private.message(StateFilter(AddFlight.arrival))
async def enter_arrival(message: types.Message, state: FSMContext):
    await state.update_data(arrival=message.text)
    await message.answer("Введите дату отправления (в формате ДД-ММ-ГГГГ):")
    await state.set_state(AddFlight.departure_date)


@my_user_private.message(StateFilter(AddFlight.departure_date))
async def enter_departure_date(message: types.Message, state: FSMContext):
    await state.update_data(departure_date=message.text)
    await message.answer("Введите дату возвращения (в формате ДД-ММ-ГГГГ):")
    await state.set_state(AddFlight.arrival_date)


@my_user_private.message(StateFilter(AddFlight.arrival_date))
async def enter_arrival_date(message: types.Message, state: FSMContext):
    await state.update_data(arrival_date=message.text)
    data = await state.get_data()
    await message.answer(f"Вы ввели следующие данные:\n"
                         f"Город отправления: {data['departure']}\n"
                         f"Пункт назначения: {data['arrival']}\n"
                         f"Дата отправления: {data['departure_date']}\n"
                         f"Дата возвращения: {data['arrival_date']}",
                         reply_markup=reply.start_kb, resize_keyboard=True)
    await state.clear()


@my_user_private.callback_query(MyCallback.filter(F.foo == "favorites"))
async def favorites_cmd(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer("Вот список ваших избранных рейсов.")


@my_user_private.callback_query(MyCallback.filter(F.foo == "track"))
async def track_cmd(query: types.CallbackQuery):
    await query.message.answer("Введите информацию о рейсе, который хотите добавить в избранное.")


@my_user_private.callback_query(MyCallback.filter(F.foo == "untrack"))
async def untrack_cmd(query: types.CallbackQuery):
    await query.message.answer("Введите информацию о рейсе, который хотите удалить из избранного.")


@my_user_private.callback_query(MyCallback.filter(F.foo == "notifications"))
async def notifications_cmd(query: types.CallbackQuery):
    await query.message.answer("Настройте уведомления о снижении или повышении цен.")


@my_user_private.callback_query(MyCallback.filter(F.foo == "settings"))
async def settings_cmd(query: types.CallbackQuery):
    await query.message.answer("Настройки бота.")


@my_user_private.callback_query(MyCallback.filter(F.foo == "about"))
async def about_cmd(query: types.CallbackQuery):
    await query.message.answer(ABOUT_BOT)


@my_user_private.callback_query(MyCallback.filter(F.foo == "help"))
async def help_cmd(query: types.CallbackQuery):
    await query.message.answer(HELP)

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
