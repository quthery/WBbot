from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


main = [
  KeyboardButton(text='Добавить API wildberries🔌'),
  KeyboardButton(text='FAQ📖'),
	KeyboardButton(text='Начать ожидание заказов⌚')

]


articles_manage_buttons = ReplyKeyboardMarkup(
	keyboard=[
		[KeyboardButton(text="Добавить артикул➕")],
		[KeyboardButton(text="Убрать артикул➖")],
		[KeyboardButton(text="Статистика📈")]
	],
	resize_keyboard=True
)

async def main_buttons(api_names: list[str]):
	keyboard = ReplyKeyboardBuilder()
	for api_name in api_names:
		keyboard.add(KeyboardButton(text=api_name, callback_data="m_"+api_name, callable="m_"+api_name))
	for main_button in main:
		keyboard.add(main_button)
	return keyboard.adjust(1).as_markup(resize_keyboard=True)
	
	