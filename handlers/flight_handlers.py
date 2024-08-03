from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from common.common import AddFlight, handle_city_selection
from filters.chat_types import ChatTypeFilter
from keyboards import reply
from keyboards.reply import MyCallback

my_flight_router = Router()
my_flight_router.message.filter(ChatTypeFilter(['private']))


@my_flight_router.callback_query(StateFilter(None), MyCallback.filter(F.foo == "search"))
async def departure_search_cmd(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(
        "Введите город отправления, пункт назначения и даты поездки для поиска билетов.\n"
        "Откуда вы хотите полететь?"
    )
    await state.set_state(AddFlight.waiting_for_city)


@my_flight_router.message(StateFilter(AddFlight.waiting_for_city))
async def handle_search_text(message: types.Message, state: FSMContext):
    await handle_city_selection(
        message, state, AddFlight.departure, "Выберите конкретный город отправления:"
    )


@my_flight_router.callback_query(StateFilter(AddFlight.departure), MyCallback.filter())
async def select_departure_city(query: types.CallbackQuery, callback_data: MyCallback, state: FSMContext):
    selected_city = callback_data.foo
    await state.update_data(departure=selected_city)
    await query.message.answer(f"Вы выбрали город отправления: {selected_city}\nКуда вы хотите полететь?")
    await state.set_state(AddFlight.arrival)


@my_flight_router.message(StateFilter(AddFlight.arrival))
async def handle_arrival_city(message: types.Message, state: FSMContext):
    await handle_city_selection(
        message, state, AddFlight.waiting_for_arrival_city, "Выберите конкретный город назначения:"
    )


@my_flight_router.callback_query(StateFilter(AddFlight.waiting_for_arrival_city), MyCallback.filter())
async def select_arrival_city(query: types.CallbackQuery, callback_data: MyCallback, state: FSMContext):
    selected_city = callback_data.foo
    await state.update_data(arrival=selected_city)
    await query.message.answer(
        f"Вы выбрали город назначения: {selected_city}"
    )
    await query.message.answer(
        "Выберите тип вашей поездки:",
        reply_markup=reply.type_trip
    )
    await state.set_state(AddFlight.type_trip)


@my_flight_router.callback_query(StateFilter(AddFlight.type_trip), MyCallback.filter())
async def select_type_trip(query: types.CallbackQuery, callback_data: MyCallback, state: FSMContext):
    trip_type = callback_data.foo
    await state.update_data(trip_type=trip_type)

    response_text = "Неизвестный тип поездки."
    if trip_type == 'one_way':
        response_text = "Вы выбрали билет в одну сторону ✈️."
    elif trip_type == 'return_way':
        response_text = "Вы выбрали возвратный билет ✈️🔄."

    await query.message.answer(response_text)

    if trip_type in ['one_way', 'return_way']:
        await query.message.answer("Сколько человек будет путешествовать? (введите число)")
        await state.set_state(AddFlight.waiting_for_adults)


@my_flight_router.message(StateFilter(AddFlight.waiting_for_adults))
async def handle_adults(message: types.Message, state: FSMContext):
    try:
        answer = int(message.text)
        await state.update_data(adults=answer)
        await state.set_state(AddFlight.departure_date)
        await message.answer("Введите дату отправления (в формате ГГГГ-ММ-ДД):")
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")


@my_flight_router.message(StateFilter(AddFlight.departure_date))
async def enter_departure_date(message: types.Message, state: FSMContext):
    data = await state.get_data()
    trip_type = data.get('trip_type')

    await state.update_data(departure_date=message.text)

    if trip_type == 'return_way':
        await state.set_state(AddFlight.arrival_date)
        await message.answer("Введите дату возвращения (в формате ГГГГ-ММ-ДД):")
    else:
        await message.answer(
            f"Вы ввели следующие данные:\n"
            f"Город отправления: {data['departure']}\n"
            f"Пункт назначения: {data['arrival']}\n"
            f"Дата отправления: {message.text}",
            reply_markup=reply.start_kb, resize_keyboard=True
        )
        await state.clear()


@my_flight_router.message(StateFilter(AddFlight.arrival_date))
async def enter_arrival_date(message: types.Message, state: FSMContext):
    await state.update_data(arrival_date=message.text)
    data = await state.get_data()

    await message.answer(
        f"Вы ввели следующие данные:\n"
        f"Город отправления: {data['departure']}\n"
        f"Пункт назначения: {data['arrival']}\n"
        f"Дата отправления: {data['departure_date']}\n"
        f"Дата возвращения: {message.text}",
        reply_markup=reply.start_kb, resize_keyboard=True
    )
    await state.clear()
