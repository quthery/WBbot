from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart


router = Router()



@router.message(CommandStart())
async def start_message(message: Message):
	await message.answer(f"Hello {message.from_user.full_name}")