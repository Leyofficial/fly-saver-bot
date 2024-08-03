from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MyCallback(CallbackData, prefix="my"):
    foo: str


class Action(str, Enum):
    start = "запуск"
    help = "помощь"
    search = "поиск"
    favorite = "избранные"
    add = "добавить"
    delete = "удалить"
    notification = "уведомления"
    settings = "настройки"
    about = "о нас"


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


def get_departures_city(cities):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text=item['presentation']['suggestionTitle'],
                callback_data=MyCallback(foo=item['presentation']['suggestionTitle']).pack()
            )] for item in cities
        ]
    )
    return keyboard
