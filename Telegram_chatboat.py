# # go to Telegram app > Search Botfather>write >start> write /newbot >mylivebot24>write bur bot name(like MyChattBot_bot)
import os
import logging  # logging :: it will log all informatipn in backed
from aiogram import Bot,Dispatcher,types
from groq import Groq
import asyncio
from aiogram.filters import Command
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv() #Load my api_key

import logging
logging.basicConfig(level=logging.DEBUG)


client = Groq(api_key=os.getenv('GROQ_API_KEY'))
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
print(TELEGRAM_BOT_TOKEN) #go to anaconda>
# create conda -n telegramchatbot python=3.7(this suppors executor)

class Reference:
     '''
    A class to store previously response from the Groq API
    '''
     def __init__(self) ->None:
          self.response = ''

reference = Reference()
model_name = 'llama-3.1-70b-versatile'

# Authentication code (to connect with telegrambot)>>>>>>>>
# Initialize bot & dispatcher
# 1) from aiogram i imported Bot becoz c-connect with telegram
bot = Bot(token=TELEGRAM_BOT_TOKEN) #This Bot will Initialise(authenticate) with my credentials (API token
dispatcher = Dispatcher()  #Dispatcher=Means Synchronization(Mean whatever message i wanna pass it will go to my telegram bot)


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)

# In python "async" & "await" used for writing Asynchronous code which allows program to handle task like I/O
#  (File reading/web request)
# 1) async : used to define asynchronous code(function that can pause or resume later)
#             async def fetch_data():
#                    # Some async task
# 2) await : used to pause execution of async function until awaited task is completed
#             async def main():
#                  data = await fetch_data()
#  asynct & await used for: concurrent operation like download multiple files,database queries,handlinh multiple request
        

# ****async & await ::: you update anything in your code so you don't need to send request, it will automatiucally sense & get updated****


def clear_past():
      """A function to clear the previous conversation and context.
    """
      reference.response = ''

@dispatcher.message(Command('clear'))
async def clear(message:types.Message):
     """
    A handler to clear the previous conversation and context.
    """
     clear_past()
     await message.reply("I've cleared the past conversation and context.")

@dispatcher.message(Command('start'))
async def welcome(message:types.Message):
     """
    This handler receives messages with `/start` or  `/help `command
    """
     await message.reply('Hey!\nI am Tele Bot created by Mr.Prathmesh. How can i assist you?')

@dispatcher.message(Command('help'))
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm Telegram bot created by Bappy! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)

# Main function
async def main():                       #dispatcher is the object responsible for managing incoming updates (such as messages),
    """Run the bot."""
    # Start the polling process
    await dispatcher.start_polling(bot) #Polling is a technique where the bot keeps checking the server for new messages ..
# start_polling() starts the process that allows the bot to continuously listen for new messages and respond to them in real-time.

# @dispatcher.messasge()
# async def chatgpt(message: types.Message):
#     """
#     A handler to process the user's input and generate a response using the chatGPT API.
#     """
#     print(f">>> USER: \n\t{message.text}")
#     client1 = Groq(api_key=os.getenv('GROQ_API_KEY'))
#     response = client1.chat.completions.create(
#         model = 'llama-3.1-70b-versatile',
#         messages = [
#             {"role": "assistant", "content": reference.response}, # role assistant
#             {"role": "user", "content": message.text} #our query 
#         ]
#     )
#     reference.response = response.choices[0].message.content
#     print(f">>> chatGPT: \n\t{reference.response}")
#     await bot.send_message(chat_id = message.chat.id, text = reference.response)


# if __name__ == "__main__":
#     asyncio.run(main())  #ayncio.run(main()): This runs the main() function, which starts the polling process and keeps the bot running.

#message.chat.id ensures the response goes to the correct user (the one who sent the message).
# await ensures the program waits until the message is sent before proceeding.



@dispatcher.message()
async def Gemini(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    cl = genai.GenerativeModel('gemini-1.5-flash')
    response = cl.generate_content(message.text)
    reference.response = response.text
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)


if __name__ == "__main__":
    asyncio.run(main())  #ayncio.run(main()): This runs the main() function, which starts the polling process and keeps the bot running.
