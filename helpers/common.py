from utils.date_format import format_datetime, format_date
from typing import Dict, Any

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import get_departures_city, get_summary_data_kb
from requests_to_api.get_airports_info import get_all_airports
from requests_to_api.get_flight_info import get_summary_results


class AddFlight(StatesGroup):
    """Состояние приложения (FSM)"""
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
    """Запрашивает данные о всех аэропортов в указанном городе."""
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


async def fetch_flight_data(flight_id: str, res: Dict[str, any]):
    """Извлекает данные о рейсе из состояния."""
    flights = res['flights']
    if flights and flights['itineraries']:
        for flight in flights['itineraries']:
            if flight['legs'][0]['segments'][0]['flightNumber'] == flight_id:
                return flight
    return None


def filter_flights_info(data):
    """Сортирует данные по убыванию цены Дешевые-Дорогие билеты"""
    res = sorted(data['itineraries'], key=lambda flight: flight['price']['raw'])
    return {"itineraries": res}


async def get_result_info(message, state, res):
    """Получает результат всех рейсов которые летят с указанных пользователям аэропортов"""
    if res and res.get('data'):
        flight_count = res['data']['context']['totalResults']
        if flight_count > 0:
            await message.answer(
                "✅✈️ Найденные рейсы:\n\n"
                "Вот и они! Выберите интересующий вас рейс из списка ниже.",
                reply_markup=get_summary_data_kb(filter_flights_info(res['data'])),
            )
            await state.update_data(flights=res['data'])
        else:
            await message.answer(
                "❌ К сожалению, рейсов не найдено.\n\n"
                "Попробуйте изменить параметры поиска и повторить попытку."
            )

    else:
        await message.answer('❌ Произошла ошибка. Пожалуйста, попробуйте еще раз позже. /start')
        await state.clear()


async def handle_flight_date(message: types.Message, state: FSMContext, date_type: str):
    """Запрашивает дату возращение если пользователь выбрал что его билет return"""
    await state.update_data(**{date_type: message.text})
    data = await state.get_data()

    if date_type == 'departure_date' and data.get('trip_type') == 'return_way':
        await state.set_state(AddFlight.arrival_date)
        await message.answer("Введите дату возвращения (в формате ГГГГ-ММ-ДД):")
    else:
        await message.answer("🛫 Запрос отправлен! Мы ищем рейсы для вас. Пожалуйста, подождите немного. ⌛")
        if data:
            res = get_summary_results(data)
            await get_result_info(message, state, res)


def handle_trip_type(trip_type: str):
    """Проверяет тип поездки"""
    response_text = "❌ Неизвестный тип поездки."
    if trip_type == 'one_way':
        response_text = "✅ Вы выбрали билет в одну сторону ✈️."
    elif trip_type == 'return_way':
        response_text = "✅ Вы выбрали возвратный билет ✈️🔄."

    return response_text


def extract_flight_info(flight_data: Dict[str, Any]) -> Dict[str, str]:
    """Извлекает информацию о рейсе из данных."""
    flight_leg = flight_data['legs'][0]
    company = flight_leg['carriers']['marketing'][0]['name']
    departure_city = flight_leg['origin']['name']
    arrival_city = flight_leg['destination']['name']
    duration = f"{flight_leg['durationInMinutes']} мин"
    departure_time = format_datetime(flight_leg['departure'])
    arrival_time = format_datetime(flight_leg['arrival'])
    price = flight_data['price']['formatted']

    departure_date = format_date(flight_leg['departure'])
    return_date = "В одну сторону."
    if len(flight_data['legs']) > 1:
        return_leg = flight_data['legs'][1]
        return_date = format_date(return_leg['departure'])

    return {
        'company': company,
        'departure_city': departure_city,
        'arrival_city': arrival_city,
        'duration': duration,
        'departure_time': departure_time,
        'arrival_time': arrival_time,
        'departure_date': departure_date,
        'return_date': return_date,
        'price': price
    }
