from app.keyboards.ReplyKeyboard import main_buttons, articles_manage_buttons
from app.keyboards.InlineKeyboard import cancel_buttons
from app.database.repository import Repository as rep
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.wildberries.marketplace import fetch_sales
from aiogram import Router, F
from aiogram.types import Message

artRouter = Router()


class choice(StatesGroup):
    api_key = State()
    choice = State()
    

@artRouter.message(F.text.regexp(r"^m_.*"))
async def testik(message: Message, state: FSMContext):
    api_key = list(await rep.get_api_key(message.from_user.id, message.text))[0]
    await state.update_data(api_key=api_key)
    display_name = str(message.text).split("_")[1]
    await message.answer(f"вы вошли в настройки магазина {display_name}🛒", reply_markup=articles_manage_buttons)
    await message.answer("Что бы вернуться в настройки нажмите кнопку ниже⬇️", reply_markup=cancel_buttons)
    await state.set_state(choice.choice)
    
@artRouter.message(choice.choice)
async def choice_state(message: Message, state: FSMContext):
    await state.update_data(choice=message.text)
    data = await state.get_data()
    if message.text == "Статистика📈":
        totalPrice = 0
        SalesOn = 0
        items = await fetch_sales(api_key=data['api_key'])
        for item in items:
            totalPrice += int(item['finishedPrice'])
            SalesOn += int(item['priceWithDisc'])
        await message.answer(f"Статистика за месяц📊\nКол-во продаж: {len(items)}\nИтого продано на: {totalPrice}rub\nПродано без скидок и т.д. на {SalesOn}rub")
            
    else:
        await message.answer("недопустимая функция!")
    