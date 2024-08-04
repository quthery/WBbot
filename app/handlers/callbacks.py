from aiogram.types import Message, CallbackQuery
from app.database.repository import Repository as rep
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from app.keyboards.ReplyKeyboard import main_buttons

CallbacksRouter = Router()


@CallbacksRouter.callback_query(F.data == "cancel")
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    api_names = await rep.get_api_names(call.from_user.id)
    await call.message.answer("Вы вернулись в главное меню", 
                reply_markup=await main_buttons(list(api_names)))
