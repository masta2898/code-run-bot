import asyncio
import logging

from aiogram import Bot as AiogramBot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

from coding_session import CodingSession


class CodeRunBot:
    def __init__(self, token, host, port, webhook_host, webhook_path):
        self.token = token
        self.host = host
        self.port = port
        self.webhook_path = webhook_path
        self.webhook_url = f"{webhook_host}{webhook_path}"

        loop = asyncio.get_event_loop()
        self.bot = AiogramBot(token=token, loop=loop)
        self.dispatcher = Dispatcher(self.bot)

        self.sessions: {int: CodingSession} = dict()
        self.default_session = CodingSession()

    def run(self):
        logging.basicConfig(level=logging.DEBUG)
        start_webhook(dispatcher=self.dispatcher, webhook_path=self.webhook_path, on_startup=self.__on_startup,
                      on_shutdown=self.__on_shutdown, skip_updates=True, host=self.host, port=self.port)

    async def __on_startup(self, dispatcher):
        await self.bot.set_webhook(self.webhook_url)
        self.__register_commands()
        logging.info("Starting up.")

    async def __on_shutdown(self, dispatcher):
        logging.info("Shutting down.")

    def __register_commands(self):
        handlers = {
            self.__echo: ['echo'],
            self.__handle_code: ['code'],
            self.__install_package: ['add'],
            self.__get_history: ['history'],
            self.__save_history: ['save'],
            self.__clear_history: ['clear'],
            self.__load_history: ['load'],
        }

        for handler, commands in handlers.items():
            self.dispatcher.register_message_handler(handler, commands=commands)

    async def __echo(self, message: types.Message):
        await self.bot.send_message(message.chat.id, message.text)

    async def __handle_code(self, message: types.Message):
        chat_id = message.chat.id
        if chat_id not in self.sessions:
            self.sessions[chat_id] = CodingSession()

        code = message.get_args()
        result = self.sessions[chat_id].code_run(code)
        if result:
            await self.bot.send_message(chat_id, result)

    async def __install_package(self, message: types.Message):
        package_name = message.get_args()
        self.default_session.add_library(package_name)
        await self.bot.send_message(message.chat.id, f"Package {package_name} has been installed.")

    async def __get_history(self, message: types.Message):
        chat_id = message.chat.id
        if chat_id not in self.sessions:
            await self.bot.send_message(chat_id, "History not found :(")
            return

        history = self.sessions[chat_id].history()
        if not history:
            await self.bot.send_message(chat_id, "Session has been created, but no history recorded.")
            return

        entities = message.entities
        hashtags = str()
        for entity in entities:
            if entity.type == "hashtag":
                hashtags += f"{entity.get_text(message.text)}\n"

        if hashtags:
            history = f"{hashtags}{history}"
            del self.sessions[chat_id]
            self.sessions[chat_id] = CodingSession()
            result = self.sessions[chat_id].code_run(history)
            if result:
                await self.bot.send_message(chat_id, result)

        await self.bot.send_message(chat_id, history)

    async def __save_history(self, message: types.Message):
        await self.bot.send_message(message.chat.id, "Not implemented yet.")

    async def __clear_history(self, message: types.Message):
        chat_id = message.chat.id
        if chat_id not in self.sessions:
            await self.bot.send_message(chat_id, "No history to clear :(")
            return

        del self.sessions[chat_id]
        await self.bot.send_message(chat_id, "History has been cleared!")

    async def __load_history(self, message: types.Message):
        chat_id = message.chat.id
        reply = message.reply_to_message
        if not reply:
            await self.bot.send_message(chat_id, "Reply to the history message with /load command to load it.")
            return

        if chat_id in self.sessions:
            del self.sessions[chat_id]
            await self.bot.send_message(chat_id, "Old history has been cleared!")

        self.sessions[chat_id] = CodingSession()
        code = reply.text
        result = self.sessions[chat_id].code_run(code)
        if result:
            await self.bot.send_message(chat_id, result)

        await self.bot.send_message(chat_id, "Code has been loaded.")
