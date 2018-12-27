import asyncio
import logging
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

from coding_session import CodingSession

API_TOKEN = '782542203:AAHz3rCUYBgHW_WePqy6F47jGxg1g9FtAuQ'

# webhook settings
WEBHOOK_HOST = ' https://code-run-bot.herokuapp.com/'
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT')

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop)
dp = Dispatcher(bot)

PYTHON_CODE_MARK = "[py]"

coding_session: CodingSession = CodingSession()


@dp.message_handler(commands='echo')
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


@dp.message_handler()
async def handle_code(message: types.Message):
    if str(message.text).startswith(PYTHON_CODE_MARK):
        code = str(message.text)[len(PYTHON_CODE_MARK):]
        result = coding_session.code_run(code)
        await bot.send_message(message.chat.id, result)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH, on_startup=on_startup, on_shutdown=on_shutdown,
                  skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT)
