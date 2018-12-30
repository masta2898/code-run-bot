import inspect
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

        self.__handlers = {
            self.__help: ['help'],
            self.__echo: ['echo', 'e'],
            self.__handle_code: ['code', 'c'],
            self.__install_package: ['add', 'a'],
            self.__get_history: ['history', 'h'],
            self.__save_history: ['save', 's'],
            self.__clear_history: ['clear', 'c'],
            self.__load_history: ['load', 'l'],
        }

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
        for handler, commands in self.__handlers.items():
            self.dispatcher.register_message_handler(handler, commands=commands)

    async def __help(self, message: types.Message):
        """Get this help message."""
        help_text = str()
        for handler, commands in self.__handlers.items():
            help_text += " ".join(f"/{command}" for command in commands)
            help_text += f" - {inspect.getdoc(handler)}\n"

        if help_text:
            help_text = f"List of bot's commands:\n{help_text}"
            await self.bot.send_message(message.chat.id, help_text)

    async def __echo(self, message: types.Message):
        """Repeats your message."""
        await self.bot.send_message(message.chat.id, message.get_args())

    async def __handle_code(self, message: types.Message):
        """Executes code, prints it's result if not None and saves it to current session."""
        chat_id = message.chat.id
        if chat_id not in self.sessions:
            self.sessions[chat_id] = CodingSession()

        code = message.get_args()
        result = self.sessions[chat_id].code_run(code)
        if result:
            await self.bot.send_message(chat_id, result)

    async def __install_package(self, message: types.Message):
        """Installs package using pip."""
        package_name = message.get_args()
        self.default_session.add_library(package_name)
        await self.bot.send_message(message.chat.id, f"Package {package_name} has been installed.")

    async def __get_history(self, message: types.Message):
        """Prints code history from current session."""
        chat_id = message.chat.id
        if chat_id not in self.sessions:
            await self.bot.send_message(chat_id, "History not found :(")
            return

        history = self.sessions[chat_id].history()
        if not history:
            await self.bot.send_message(chat_id, "Session has been created, but no history recorded.")
            return

        hashtags = self.__get_hashtags(message)
        if hashtags:
            history = f"{hashtags}{history}"
            await self.__update_session(chat_id, history)

        await self.bot.send_message(chat_id, history)

    async def __save_history(self, message: types.Message):
        """Saves history via specified method."""
        await self.bot.send_message(message.chat.id, "Not implemented yet.")

    async def __clear_history(self, message: types.Message):
        """Clears current session and creates new."""
        chat_id = message.chat.id
        if chat_id not in self.sessions:
            await self.bot.send_message(chat_id, "No history to clear :(")
            return

        await self.__update_session(chat_id, "")
        await self.bot.send_message(chat_id, "History has been cleared!")

    async def __load_history(self, message: types.Message):
        """Loads code from replied message to session wiping old code."""
        chat_id = message.chat.id
        reply = message.reply_to_message
        if not reply:
            await self.bot.send_message(chat_id, "Reply to the history message with /load command to load it.")
            return

        if chat_id in self.sessions:
            del self.sessions[chat_id]
            await self.bot.send_message(chat_id, "Old history has been cleared!")

        await self.__update_session(chat_id, reply.text)
        await self.bot.send_message(chat_id, "Code has been loaded.")

    async def __update_session(self, chat_id, code):
        if chat_id in self.sessions:
            del self.sessions[chat_id]

        self.sessions[chat_id] = CodingSession()
        result = self.sessions[chat_id].code_run(code)
        if result:
            await self.bot.send_message(chat_id, result)

    def __get_hashtags(self, message: types.Message):
        hashtags = str()
        entities = message.entities
        for entity in entities:
            if entity.type == "hashtag":
                hashtags += f"{entity.get_text(message.text)}\n"
        return hashtags
