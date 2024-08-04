from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup


inline_keyboard = [
    [InlineKeyboardButton(text="Назад", callback_data="cancel")]
]

cancel_buttons = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


