from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from common.common import AddFlight
from filters.chat_types import ChatTypeFilter
from handlers.user_private import handle_city_selection
from keyboards import reply
from keyboards.reply import MyCallback

my_arrival_private = Router()
my_arrival_private.message.filter(ChatTypeFilter(['private']))


@my_arrival_private.message(StateFilter(AddFlight.arrival))
async def handle_arrival_city(message: types.Message, state: FSMContext):
    await handle_city_selection(
        message, state, AddFlight.waiting_for_arrival_city, "Выберите конкретный город назначения:"
    )


@my_arrival_private.callback_query(StateFilter(AddFlight.waiting_for_arrival_city), MyCallback.filter())
async def select_arrival_city(query: types.CallbackQuery, callback_data: MyCallback, state: FSMContext):
    selected_city = callback_data.foo
    await state.update_data(arrival=selected_city)
    await query.message.answer(
        f"Вы выбрали город назначения: {selected_city}\nВведите дату отправления (в формате ДД-ММ-ГГГГ):"
    )
    await state.set_state(AddFlight.departure_date)


@my_arrival_private.message(StateFilter(AddFlight.arrival_date))
async def enter_arrival_date(message: types.Message, state: FSMContext):
    await state.update_data(arrival_date=message.text)
    data = await state.get_data()
    await message.answer(
        f"Вы ввели следующие данные:\n"
        f"Город отправления: {data['departure']}\n"
        f"Пункт назначения: {data['arrival']}\n"
        f"Дата отправления: {data['departure_date']}\n"
        f"Дата возвращения: {data['arrival_date']}",
        reply_markup=reply.start_kb, resize_keyboard=True
    )
    await state.clear()