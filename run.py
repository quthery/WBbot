import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from app.handlers.handlers import router
from app.handlers.reg import fsmRouter
from app.handlers.manage_art import artRouter
from app.handlers.callbacks import CallbacksRouter
from app.database.init import create_tables



async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_routers(router, fsmRouter, artRouter, CallbacksRouter)
    await create_tables()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        print("Bot is active!")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is off")
