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
            InlineKeyboardButton(text="Запуск 🚀", callback_data='запуск'),
            InlineKeyboardButton(text="Помощь ❓", callback_data=MyCallback(foo='помощь').pack()),
            InlineKeyboardButton(text="Поиск авиабилетов 🔍", callback_data=MyCallback(foo='поиск').pack()),
        ],
        [
            InlineKeyboardButton(text="Избранные рейсы 💼", callback_data='избранные'),
            InlineKeyboardButton(text="Добавить рейс ➕", callback_data='добавить'),
            InlineKeyboardButton(text="Удалить рейс ❌", callback_data='удалить'),
        ],
        [
            InlineKeyboardButton(text="Уведомления 📢", callback_data='уведомления'),
            InlineKeyboardButton(text="Настройки ⚙️", callback_data='настройки'),
            InlineKeyboardButton(text="О нас ℹ️", callback_data='о нас'),
        ],
    ],
)
