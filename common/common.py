from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import get_departures_city
from requests_to_api.get_airports_info import get_all_airports


class AddFlight(StatesGroup):
    departure = State()
    waiting_for_city = State()
    arrival = State()
    waiting_for_arrival_city = State()
    type_trip = State()
    adults = State()
    waiting_for_adults = State()
    departure_date = State()
    arrival_date = State()


async def handle_city_selection(message: types.Message, state: FSMContext, next_state: State, prompt: str):
    user_city = message.text
    res = get_all_airports(user_city)

    if res and res.get('status') and len(res['airports']) > 0:
        await message.answer(
            prompt,
            reply_markup=get_departures_city(res['airports'])
        )
        await state.set_state(next_state)
    else:
        await message.answer("❌ Извините, не удалось найти аэропорты для данного города.")
        await message.answer("Введите аэропорт еще раз:")
