from utils.date_format import format_datetime, format_date
from typing import Dict, Any

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import get_departures_city, get_summary_data_kb
from requests_to_api.get_airports_info import get_all_airports
from requests_to_api.get_flight_info import get_summary_results


class AddFlight(StatesGroup):
    """Application States (FSM)"""
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
    """Requests airport information for the specified city."""
    user_city = message.text
    res = get_all_airports(user_city)

    if res and res.get('status') and len(res['airports']) > 0:
        await message.answer(
            prompt,
            reply_markup=get_departures_city(res['airports'])
        )
        await state.set_state(next_state)
    else:
        await message.answer("❌ Sorry, we couldn't find any airports for this city.")
        await message.answer("Please enter the airport again:")


async def fetch_flight_data(flight_id: str, res: Dict[str, any]):
    """Extracts flight data from the response."""
    flights = res['flights']
    if flights and flights['itineraries']:
        for flight in flights['itineraries']:
            if flight['legs'][0]['segments'][0]['flightNumber'] == flight_id:
                return flight
    return None


def filter_flights_info(data):
    """Sorts flight data by price in ascending order."""
    res = sorted(data['itineraries'], key=lambda flight: flight['price']['raw'])
    return {"itineraries": res}


async def get_result_info(message, state, res):
    """Gets the result of all flights from the specified airports."""
    if res and res.get('data'):
        flight_count = res['data']['context']['totalResults']
        if flight_count > 0:
            await message.answer(
                "✅✈️ Found flights:\n\n"
                "Here they are! Choose a flight from the list below.",
                reply_markup=get_summary_data_kb(filter_flights_info(res['data'])),
            )
            await state.update_data(flights=res['data'])
        else:
            await message.answer(
                "❌ Unfortunately, no flights were found.\n\n"
                "Try adjusting the search parameters and try again."
            )
    else:
        await message.answer(
            '❌ An error occurred. Please try again later. /start'
        )
        await state.clear()


async def handle_flight_date(message: types.Message, state: FSMContext, date_type: str):
    """Requests return date if the user selected a return ticket."""
    await state.update_data(**{date_type: message.text})
    data = await state.get_data()

    if date_type == 'departure_date' and data.get('trip_type') == 'return_way':
        await state.set_state(AddFlight.arrival_date)
        await message.answer("📅 Enter the return date (in YYYY-MM-DD format):")
    else:
        await message.answer("🛫 Request sent! We are searching for flights for you. Please wait a moment. ⌛")
        if data:
            res = get_summary_results(data)
            await get_result_info(message, state, res)


def handle_trip_type(trip_type: str):
    """Checks the trip type."""
    response_text = "❌ Unknown trip type."
    if trip_type == 'one_way':
        response_text = "✅ You selected a one-way ticket ✈️."
    elif trip_type == 'return_way':
        response_text = "✅ You selected a return ticket ✈️🔄."

    return response_text


def extract_flight_info(flight_data: Dict[str, Any]) -> Dict[str, str]:
    """Extracts flight information from the data."""
    flight_leg = flight_data['legs'][0]
    company = flight_leg['carriers']['marketing'][0]['name']
    departure_city = flight_leg['origin']['name']
    arrival_city = flight_leg['destination']['name']
    duration = f"{flight_leg['durationInMinutes']} mins"
    departure_time = format_datetime(flight_leg['departure'])
    arrival_time = format_datetime(flight_leg['arrival'])
    price = flight_data['price']['formatted']

    departure_date = format_date(flight_leg['departure'])
    return_date = "One-way."
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
