from app.handlers.callbacks import CallbacksRouter
from app.handlers.manage_art import artRouter
from app.database.init import create_tables
from aiogram.methods import DeleteWebhook
from app.handlers.handlers import router
from app.handlers.reg import fsmRouter
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import asyncio
import os





async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))

    dp = Dispatcher()
    dp.include_routers(router, fsmRouter, artRouter, CallbacksRouter)
    await create_tables()
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    try:
        print("Bot is active!")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is off")
