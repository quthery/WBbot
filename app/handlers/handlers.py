from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.database.repository import Repository as rep
from app.keyboards.ReplyKeyboard import main_buttons


router = Router()


@router.message(CommandStart())
async def start_message(message: Message):
    await message.answer(
        f'🌟Привет, {message.from_user.full_name}!🌟 Ты попал в WBchecker! 🚀 '
        'Нужно больше информации? Загляни в FAQ.📖', reply_markup=await main_buttons(list(await rep.get_api_keys(message.from_user.id)))
    )
    await rep.add_user(
        id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username
    )

@router.message(F.text == "FAQ📖")
async def FAQ(message: Message):
    await message.answer("Часто задаваемые вопросы:\nhttps://telegra.ph/FAQ-WBcheckerBot-08-03", reply_markup=await main_buttons(list(await rep.get_api_keys(message.from_user.id))))
    
#Варианты реализации нажатия кнопки:
# @fsmRouter.message(Reg_api.api_name)
# async def reg_api_step3(message: Message, state: FSMContext):
#     await state.update_data(api_name=message.text)
#     data = await state.get_data()
    
#     # Debugging output
#     print(f"User ID: {message.from_user.id}, API: {data['api']}, API Name: {data['api_name']}")
    
#     await rep.add_api(user_id=message.from_user.id, api_key=data['api'], api_name=data['api_name'])
#     await state.clear()
    
#     api_keys = await rep.get_api_keys(message.from_user.id)
#     print(f"API Keys: {api_keys}")  # Debugging output
    
#     await message.answer("API ключ успешно добавлен, можете начинать работу", 
#                          reply_markup=await main_buttons(list(api_keys)))


# @fsmRouter.message(Reg_api.api_name)
# async def reg_api_step3(message: Message, state: FSMContext):
#     await state.update_data(api_name=message.text)
#     data = await state.get_data()
    
#     # Debugging output
#     print(f"User ID: {message.from_user.id}, API: {data['api']}, API Name: {data['api_name']}")
    
#     await rep.add_api(user_id=message.from_user.id, api_key=data['api'], api_name=data['api_name'])
#     await state.clear()
    
#     api_keys = await rep.get_api_keys(message.from_user.id)
#     print(f"API Keys: {api_keys}")  # Debugging output
    
#     await message.answer("API ключ успешно добавлен, можете начинать работу", 
#                          reply_markup=await main_buttons(list(api_keys)))
    
# @fsmRouter.callback_query_handler(lambda c: c.data.startswith('button_'))
# async def process_button(callback_query: CallbackQuery):
#     data = callback_query.data.split('_')
#     index = int(data[1])  # Индекс кнопки
#     text = data[2]         # Текст кнопки

#     await callback_query.answer(f'Вы нажали кнопку: {text} с индексом: {index}')


    
    
    



    
        
    

    

    







