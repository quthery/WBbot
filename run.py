import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from app.handlers.handlers import router
from app.handlers.fsm import fsmRouter
from app.database.init import create_tables
from app.wildberries.marketplace import fetch_new_orders



async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_routers(router, fsmRouter)
    await create_tables()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        print("Bot is active!")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is off")
