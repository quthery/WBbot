from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


main = [
  KeyboardButton(text='Добавить API wildberries🔌'),
  KeyboardButton(text='FAQ📖')
]

inline_keyboard = [
    [InlineKeyboardButton(text="Назад", callback_data="cancel")]
]

cancel_buttons = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

async def main_buttons(api_names: list[str]):
	keyboard = ReplyKeyboardBuilder()
	for api_name in api_names:
		keyboard.add(KeyboardButton(text=api_name, callback_data="m_"+api_name, callable="m_"+api_name))
	for main_button in main:
		keyboard.add(main_button)
	return keyboard.adjust(2).as_markup(resize_keyboard=True)
	
	