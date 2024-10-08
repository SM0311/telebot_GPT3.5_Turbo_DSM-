import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
import openai
import sys



class Reference:
    '''
    A class to store previously response from the chatGPT API
    '''

    def __init__(self) -> None:
        self.response = ""


load_dotenv()
openai.api_key = os.getenv("OpenAI_API_KEY")  

reference = Reference()

TOKEN = os.getenv("TOKEN")

# model name 
model_name = "gpt-3.5-turbo"

# initialize the bot and the dispatcher from the echo bot py
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)


def clear_past():
    '''
    A function to clear the previous context and conversation.
    '''
    reference.response=""



@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or `/help` command
    """
    
    await message.reply("Hi\nI am Tele bot!\nCreated by Suraj Mishra. How can I help you?")



@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I have cleared the past conversation and context.")


@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help  menu.
    """

    help_command = """
    Hi There, I'm chatGPT Telegram bot created by Suraj! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)


@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    
    try:
        response = openai.Completion.create(
            model=model_name,
            prompt=message.text,
            max_tokens=150
        )
        print(f">>> RAW API RESPONSE: \n\t{response}")
        reference.response = response.choices[0].text.strip()
        print(f">>> chatGPT: \n\t{reference.response}")
        await bot.send_message(chat_id=message.chat.id, text=reference.response)
    except Exception as e:
        print(f"Error: {e}")
        await bot.send_message(chat_id=message.chat.id, text="An error occurred. Please try again.")




if __name__=="__main__":
    executor.start_polling(dispatcher, skip_updates=True)