import asyncio
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN
from handlers import handle_start, handle_other_messages

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(commands=["start"])
async def start_handler(message: types.Message):
    await handle_start(message, bot)

@dp.message()
async def other_handler(message: types.Message):
    await handle_other_messages(message, bot)

async def main():
    print("🤖 KinoBot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
