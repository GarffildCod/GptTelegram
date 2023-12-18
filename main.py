
from openai import OpenAI


from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from decouple import config
import asyncio
import logging


token_tg = "Token_TELEGRAM"

token_gpt = "Token_GPT"

client = OpenAI(api_key=token_gpt)
bot = Bot(token=token_tg,parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()

router = Router()

dp.include_router(router)

messages = []


def start_chat_gpt(request, messages):
    try:
        message = str(request)
        messages.append({'role': 'user', 'content': message})
        chat = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=messages)
        answer = chat.choices[0].message.content
        messages.append({'role': 'assistant', 'content': answer})
        return answer
    except Exception as e:
        logging.error(e)


@router.message(CommandStart())
async def command_start_handler(msg: Message):
    username = msg.chat.username
    greitng = f'Hello, *{username}* I am here to help you!'

    await msg.answer(greitng, parse_mode=ParseMode.MARKDOWN)


@router.message()
async def chat_handler(msg: Message):
    try:
        loading_info = await msg.answer('Thinking... ', parse_mode=ParseMode.MARKDOWN)

        text_answer = start_chat_gpt(msg.text, messages)

        await msg.answer(text_answer, parse_mode=ParseMode.MARKDOWN)

        await bot.delete_message(msg.chat.id,loading_info.message_id)
    except Exception as ex:
        logging.error(ex)


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as ex:
        logging.error(f'Error: {ex}')
