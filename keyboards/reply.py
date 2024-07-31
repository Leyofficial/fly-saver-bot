from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Запуск 🚀"),
            KeyboardButton(text="Помощь ❓"),
            KeyboardButton(text="Поиск авиабилетов 🔍")
        ],
        [
            KeyboardButton(text="Избранные рейсы 💼"),
            KeyboardButton(text="Добавить рейс ➕"),
            KeyboardButton(text="Удалить рейс ❌")
        ],
        [
            KeyboardButton(text="Уведомления 📢"),
            KeyboardButton(text="Настройки ⚙️"),
            KeyboardButton(text="О нас ℹ️")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)
