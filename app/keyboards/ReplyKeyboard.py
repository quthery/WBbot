from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


main = [
  KeyboardButton(text='Добавить API wildberries🔌'),
  KeyboardButton(text='FAQ📖')
]


async def main_buttons(api_keys: list[str]):
	keyboard = ReplyKeyboardBuilder()
	for api_key in api_keys:
		keyboard.add(KeyboardButton(text=api_key))
	for main_button in main:
		keyboard.add(main_button)
	return keyboard.adjust(2).as_markup(resize_keyboard=True)
	
	