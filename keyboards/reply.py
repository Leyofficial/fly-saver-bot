from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.date_format import format_datetime


class MyCallback(CallbackData, prefix="my"):
    foo: str


start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Поиск авиабилетов 🔍", callback_data=MyCallback(foo='search').pack()),
        ],
        [
            InlineKeyboardButton(text="Избранные рейсы 💼", callback_data=MyCallback(foo='favorites').pack()),
            InlineKeyboardButton(text="Добавить рейс ➕", callback_data=MyCallback(foo='track').pack()),
            InlineKeyboardButton(text="Удалить рейс ❌", callback_data=MyCallback(foo='untrack').pack()),
        ],
        [
            InlineKeyboardButton(text="Уведомления 📢", callback_data=MyCallback(foo='notifications').pack()),
            InlineKeyboardButton(text="Настройки ⚙️", callback_data=MyCallback(foo='settings').pack()),
            InlineKeyboardButton(text="О нас ℹ️", callback_data=MyCallback(foo='about').pack()),
        ],
        [
            InlineKeyboardButton(text="Помощь ❓", callback_data=MyCallback(foo='help').pack()),
        ],
    ],
)

type_trip = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Возвратная ✈️🔄", callback_data=MyCallback(foo='return_way').pack()),
            InlineKeyboardButton(text="В одну сторону ✈️", callback_data=MyCallback(foo='one_way').pack()),
        ],
    ]
)


finished_search = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Новый поиск 🔍", callback_data=MyCallback(foo="search").pack())
        ]
    ]
)

def get_departures_city(cities):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text=item['presentation']['suggestionTitle'] + ' ' + item['presentation']['subtitle'],
                callback_data=MyCallback(foo=item['navigation']['relevantFlightParams']['skyId']).pack()
            )] for item in cities
        ]
    )
    return keyboard


def get_summary_data_kb(data):
    buttons = []

    for item in data['itineraries'][:10]:
        company = item['legs'][0]['carriers']['marketing'][0]['name']
        duration = str(item['legs'][0]['durationInMinutes']) + ' min'
        departure_time = format_datetime(item['legs'][0]['departure'])
        arrival_time = format_datetime(item['legs'][0]['arrival'])
        price = item['price']['formatted']
        id = item['legs'][0]['segments'][0]['flightNumber']
        text = f"🛫{company} dep {departure_time} arr {arrival_time} 🕒 {duration} 💵 {price}\n"

        button = InlineKeyboardButton(
            text=text,
            callback_data=MyCallback(foo=id).pack()
        )
        buttons.append([button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


def back_or_finish_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data=MyCallback(foo="back").pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Завершить поиск",
                    callback_data=MyCallback(foo="finish").pack()
                )
            ]
        ]
    )
    return keyboard
