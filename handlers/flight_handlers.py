from aiogram import Router, types, F
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.context import FSMContext

from helpers.common import AddFlight, handle_city_selection, fetch_flight_data, handle_flight_date, extract_flight_info, \
    get_result_info, handle_trip_type
from filters.chat_types import ChatTypeFilter
from helpers.replies_texts import FINISHED_SEARCH, FLIGHT_DETAILS_TEMPLATE
from keyboards import reply
from keyboards.reply import MyCallback, back_or_finish_kb, finished_search

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
        message, state, AddFlight.departure, "✅ Выберите конкретный город отправления:"
    )


@my_flight_router.callback_query(StateFilter(AddFlight.departure), MyCallback.filter())
async def select_departure_city(query: types.CallbackQuery, callback_data: MyCallback, state: FSMContext):
    fromId = callback_data.foo
    await state.update_data(fromIdCode=fromId)
    await query.message.answer(f"Куда вы хотите полететь?")
    await state.set_state(AddFlight.arrival)


@my_flight_router.message(StateFilter(AddFlight.arrival))
async def handle_arrival_city(message: types.Message, state: FSMContext):
    await handle_city_selection(
        message, state, AddFlight.waiting_for_arrival_city, "✅ Выберите конкретный город назначения:"
    )


@my_flight_router.callback_query(StateFilter(AddFlight.waiting_for_arrival_city), MyCallback.filter())
async def select_arrival_city(query: types.CallbackQuery, callback_data: MyCallback, state: FSMContext):
    toId = callback_data.foo
    await state.update_data(toIdCode=toId)
    await query.message.answer(
        "Выберите тип вашей поездки:",
        reply_markup=reply.type_trip
    )
    await state.set_state(AddFlight.type_trip)


@my_flight_router.callback_query(StateFilter(AddFlight.type_trip), MyCallback.filter())
async def select_type_trip(query: types.CallbackQuery, callback_data: MyCallback, state: FSMContext):
    trip_type = callback_data.foo
    await state.update_data(trip_type=trip_type)

    response_text = handle_trip_type(trip_type)
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
        await message.answer("❌ Пожалуйста, введите корректное число.")


@my_flight_router.message(StateFilter(AddFlight.departure_date))
async def enter_departure_date(message: types.Message, state: FSMContext):
    await handle_flight_date(message, state, 'departure_date')


@my_flight_router.message(StateFilter(AddFlight.arrival_date))
async def enter_arrival_date(message: types.Message, state: FSMContext):
    await handle_flight_date(message, state, 'arrival_date')


@my_flight_router.callback_query(or_f(MyCallback.filter(F.foo == "back"), MyCallback.filter(F.foo == "finish")))
async def handle_selected_on_flight(query: types.CallbackQuery, callback_data: MyCallback, state: FSMContext):
    selected = callback_data.foo
    data = await state.get_data()
    if selected == 'back':
        if data.get('flights'):
            await get_result_info(query.message, state, {"data": data['flights']})
    elif selected == 'finish':
        await state.clear()
        await query.message.answer(FINISHED_SEARCH, reply_markup=finished_search, parse_mode='Markdown')


@my_flight_router.callback_query(MyCallback.filter())
async def handle_selected_flight(query: types.CallbackQuery, callback_data: MyCallback, state: FSMContext):
    flight_id = callback_data.foo
    data = await state.get_data()
    flight_data = await fetch_flight_data(flight_id, data)

    if flight_data:
        flight_info = extract_flight_info(flight_data)
        destination_img_url = data['flights']['destinationImageUrl']

        if destination_img_url:
            await query.message.answer_photo(photo=destination_img_url, caption="Детали рейса:")

        details_text = FLIGHT_DETAILS_TEMPLATE.format(**flight_info)
        await query.message.answer(details_text, parse_mode='Markdown', reply_markup=back_or_finish_kb())
    else:
        await query.message.answer("❌ Данные о рейсе не найдены.")
