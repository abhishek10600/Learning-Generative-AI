from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
import openai
import sys
import logging
import asyncio


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

openai.api_key = OPENAI_API_KEY


class Reference:

    """
    A class to store previous response from openai API 
    """

    def __init__(self):
        self.response = ""


reference = Reference()


def clear_past():
    """A function to clear the previous conversation and context."""
    reference.response = ""


model_name = "gpt-3.5-turbo"


# Initializer bot and dispatcher
dispatcher = Dispatcher()
bot = Bot(token=TELEGRAM_BOT_TOKEN)


@dispatcher.message(CommandStart())
async def command_start_handler(message: types.Message):
    """
    This handler receives messages with `/start` or `/help` command
    """
    await message.reply("Hi\nI am Telegram Bot created by Abhishek Sharma. How can I assist you ?")


@dispatcher.message(Command(commands=["help"]))
async def helper(message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm chatGPT Telegram bot create by Abhishek Sharma. Please follow these commands -
    /start - to start a conversation.
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)


@dispatcher.message(Command(commands=["clear"]))
async def clear(message):
    """
    A handler to clear the previous conversation and context
    """
    clear_past()
    await message.reply("I have cleared the past conversation and context.")


@dispatcher.message()
async def chatgpt(message):
    """
    A handler to process the user's input and generate a response using chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "assistant", "content": reference.response},  # role assitant
            {"role": "user", "content": message.text}  # our query
        ]
    )

    reference.response = response.choices[0].message.content
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id=message.chat.id, text=reference.response)


async def main():
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
