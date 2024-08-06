from aiogram import Router, types
from string import punctuation
my_chat_procedure = Router()

RESTRICTED = {'осел', 'петух', 'козел', 'козёл', 'осёл'}


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@my_chat_procedure.message()
@my_chat_procedure.edited_message()
async def chat_procedure(message: types.Message) -> None:
    if message and RESTRICTED.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f'@{message.from_user.username}, соблюдайте порядок в чате!')
        await message.delete()
