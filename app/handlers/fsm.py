from app.keyboards.ReplyKeyboard import main_buttons, cancel_buttons

from app.database.repository import Repository as rep
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart


class Reg_api(StatesGroup):
    api_name = State()
    api = State()
    passsword = State()

class Reg_user(StatesGroup):
    password = State()
    
    
fsmRouter = Router()


@fsmRouter.message(CommandStart())
async def start_message(message: Message, state: FSMContext):
    user = await rep.get_user(message.from_user.id)
    if user != 0:
        await state.clear()
        api_names = await rep.get_api_names(message.from_user.id)
        await message.answer(
            f'🌟Привет, {message.from_user.full_name}!🌟 Ты попал в систему WBchecker! 🚀 Для навигации используй кнопки ниже',
            reply_markup=await main_buttons(list(api_names))
        )
    else:
        await message.answer(
            text=f'🌟Привет, {message.from_user.full_name}!🌟 Ты попал в систему WBchecker! 🚀 '
                 'Введи пароль, чтобы зарегистрироваться'
        )
        await state.set_state(Reg_user.password)


@fsmRouter.message(Reg_user.password)
async def register_user(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    await rep.add_user(id=message.from_user.id, full_name=message.from_user.full_name, username=message.from_user.username, password=data['password'])
    await state.clear()
    api_names = await rep.get_api_names(message.from_user.id)
    await message.answer("Вы успешно зарегистрированы можете начинать работу", 
                         reply_markup=await main_buttons(list(api_names)))





@fsmRouter.message(F.text == "Добавить API wildberries🔌")
async def reg_api_step1(message: Message, state: FSMContext):
    await state.set_state(Reg_api.api)
    await message.answer("Введите свой API ключ", reply_markup=cancel_buttons)


@fsmRouter.message(Reg_api.api)
async def reg_api_step2(message: Message, state: FSMContext):
    await state.update_data(api=message.text)
    await state.set_state(Reg_api.api_name)
    await message.answer("Введите название под которым хотите видеть свой API в боте")






@fsmRouter.message(Reg_api.api_name)
async def reg_api_step3(message: Message, state: FSMContext):
    await state.update_data(api_name="m_"+message.text)
    await message.answer("Введите пароль чтобы подтвердить")
    await state.set_state(Reg_api.passsword)


@fsmRouter.message(Reg_api.passsword)
async def reg_api_verify_pass(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    password = await rep.get_user_password(message.from_user.id)
    data = await state.get_data()
    if data['password'] != password:
        await message.answer("Вы ввели неверный пароль!")
        await state.clear()
    else:
        print(f"User ID: {message.from_user.id}, API: {data['api']}, API Name: {data['api_name']}")
        await rep.add_api(user_id=message.from_user.id, api_key=data['api'], api_name=data['api_name'])
        await state.clear()
        api_names = await rep.get_api_names(message.from_user.id)
        await message.answer("API ключ успешно добавлен, можете начинать работу", 
                reply_markup=await main_buttons(list(api_names)))

    

@fsmRouter.callback_query(F.data == "cancel")
async def cancel(call: CallbackQuery):
    await call.answer()
    api_names = await rep.get_api_names(call.message.from_user.id)
    await call.message.answer("вы вернулись в главное меню", reply_markup=await main_buttons(list(api_names)))


    