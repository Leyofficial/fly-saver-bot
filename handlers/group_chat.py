from aiogram import Router, types
from aiogram.filters import CommandStart
from filters.chat_types import ChatTypeFilter

my_group_chat = Router()
my_group_chat.message.filter(ChatTypeFilter(['channel', 'group', 'supergroup']))


@my_group_chat.message(CommandStart())
async def start_cmd(message: types.Message) -> None:
    await message.answer("Добро пожаловать наши халявщики!")
