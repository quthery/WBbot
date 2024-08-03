from app.keyboards.ReplyKeyboard import main_buttons
from app.database.repository import Repository as rep
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove


class Reg_api(StatesGroup):
    api_name = State()
    api = State()
    
    
fsmRouter = Router()

@fsmRouter.message(F.text == "Добавить API wildberries🔌")
async def reg_api_step1(message: Message, state: FSMContext):
    await state.set_state(Reg_api.api)
    await message.answer("Введите свой API ключ")


@fsmRouter.message(Reg_api.api)
async def reg_api_step2(message: Message, state: FSMContext):
    await state.update_data(api=message.text)
    await state.set_state(Reg_api.api_name)
    await message.answer("Введите название под которым хотите видеть свой API в боте")


@fsmRouter.message(Reg_api.api_name)
async def reg_api_step3(message: Message, state: FSMContext):
    await state.update_data(api_name=message.text)
    data = await state.get_data()
    print(f"User ID: {message.from_user.id}, API: {data['api']}, API Name: {data['api_name']}")
    await rep.add_api(user_id=message.from_user.id, api_key=data['api'], api_name=data['api_name'])
    await state.clear()
    api_keys = await rep.get_api_keys(message.from_user.id)
    await message.answer("API ключ успешно добавлен, можете начинать работу", 
                         reply_markup=await main_buttons(list(api_keys)))
    

