from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from common.common import AddFlight, handle_city_selection
from filters.chat_types import ChatTypeFilter
from keyboards.reply import MyCallback

my_depart_private = Router()
my_depart_private.message.filter(ChatTypeFilter(['private']))


@my_depart_private.callback_query(StateFilter(None), MyCallback.filter(F.foo == "search"))
async def departure_search_cmd(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(
        "Введите город отправления, пункт назначения и даты поездки для поиска билетов.\n"
        "Откуда вы хотите полететь?"
    )
    await state.set_state(AddFlight.waiting_for_city)


@my_depart_private.message(StateFilter(AddFlight.waiting_for_city))
async def handle_search_text(message: types.Message, state: FSMContext):
    await handle_city_selection(
        message, state, AddFlight.departure, "Выберите конкретный город:"
    )


@my_depart_private.callback_query(StateFilter(AddFlight.departure), MyCallback.filter())
async def select_departure_city(query: types.CallbackQuery, callback_data: MyCallback, state: FSMContext):
    selected_city = callback_data.foo
    await state.update_data(departure=selected_city)
    await query.message.answer(f"Вы выбрали город отправления: {selected_city}\nКуда вы хотите полететь?")
    await state.set_state(AddFlight.arrival)


@my_depart_private.message(StateFilter(AddFlight.departure_date))
async def enter_departure_date(message: types.Message, state: FSMContext):
    await state.update_data(departure_date=message.text)
    await message.answer("Введите дату возвращения (в формате ДД-ММ-ГГГГ):")
    await state.set_state(AddFlight.arrival_date)
