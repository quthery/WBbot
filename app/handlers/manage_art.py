from app.keyboards.ReplyKeyboard import articles_manage_buttons, main_buttons
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
    #в случае если пользователь выбрал убрать либо добавить артикул
    article = State()
    quantity = State()
    

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
    elif message.text == "Добавить артикул➕":
        await state.set_state(choice.article)
        await message.answer("Напишите артикул", reply_markup=cancel_buttons)
    elif message.text == "Убрать артикул➖":
        await state.set_state(choice.article)
        await message.answer("Напишите артикул", reply_markup=cancel_buttons)
    else:
        await message.answer("недопустимая функция!", reply_markup=cancel_buttons)
    
@artRouter.message(choice.article)
async def choice_art(message: Message, state: FSMContext):
    await state.update_data(article=message.text)
    await message.answer("Какое количество на складе?", reply_markup=cancel_buttons)
    await state.set_state(choice.quantity)

@artRouter.message(choice.quantity)
async def choice_quantity(message: Message, state: FSMContext):
    try:
        int(message.text)
    except ValueError:
        await message.answer("Введите пожалуйста число!", reply_markup=cancel_buttons)
        await state.set_state(choice.quantity)
        return
    await state.update_data(quantity=message.text)
    data = await state.get_data()
    if data['choice'] == "Добавить артикул➕":
        await rep.add_article_count(token=data['api_key'], art=data['article'], count=data['quantity'])
        api_names = await rep.get_api_names(message.from_user.id)
        await message.answer(f"Артикул {data['article']}, успешно добавлено {data['quantity']} штук💼", reply_markup=await main_buttons(list(api_names)))
        
        await state.clear()
    elif data['choice'] == "Убрать артикул➖":
        code = await rep.minus_article_to_sklad(data['article'], int(data['quantity']), data['api_key'])
        if code == 404:
            await message.answer("Такого артикула нет в базе данных❗\nвозможно вы ошиблись попробуйте заново ввести артикул📓")
            await state.set_state(choice.article)
        elif code == 400:
            await message.answer("Артикул успешно удален из базы данных💥")
            await state.set_state(choice.article)
        else:
            await message.answer(f"Артикул {data['article']}, успешно убрано {data['quantity']} штук💼")

    

