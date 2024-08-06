from aiogram.types import BotCommand

private = [
    BotCommand(command="start", description="Запуск бота и приветственное сообщение"),
    BotCommand(command="help", description="Посмотреть меню"),
    BotCommand(command="search", description="Поиск авиабилетов"),
    BotCommand(command="favorites", description="Просмотр списка избранных рейсов"),
    BotCommand(command="track", description="Добавить рейс в избранное"),
    BotCommand(command="untrack", description="Удалить рейс из избранного"),
    BotCommand(command="notifications", description="Настройка уведомлений"),
    BotCommand(command="settings", description="Настройки бота"),
    BotCommand(command="about", description="О нас")
]
