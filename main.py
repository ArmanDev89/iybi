import logging
import aiogram
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncio
import aiosqlite  

previous_data = ""

API_TOKEN = '6683272705:AAGifOe-3_RmPV0ZCCEyoLoFjHqi3F1kOJs'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

async def get_data_from_db():
    async with aiosqlite.connect('server.db') as db:
        async with db.execute("SELECT * FROM Data") as cursor:
            return await cursor.fetchall()

async def send_data_to_user(user_id, data):
    await bot.send_message(user_id, data)

@dp.message_handler(commands=['start'])
async def hello(message: types.Message):
    await bot.send_message(text="HELLO", chat_id=1681492678)

async def check_for_new_data():
    global previous_data
    while True:
        data = await get_data_from_db()
        if data != previous_data:
            await send_data_to_user(1681492678, f"Ученик {data[len(data)-1][0]} был освобожден по причине болезни: {data[len(data)-1][1]}")
            previous_data = data
        await asyncio.sleep(10) 

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check_for_new_data())
    executor.start_polling(dp, skip_updates=True)
    loop.run_forever()
