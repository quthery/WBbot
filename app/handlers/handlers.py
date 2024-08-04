from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from app.database.repository import Repository as rep
from app.keyboards.ReplyKeyboard import main_buttons


router = Router()



@router.message(F.text == "FAQ📖")
async def FAQ(message: Message):
    await message.answer("Часто задаваемые вопросы:\nhttps://telegra.ph/FAQ-WBcheckerBot-08-03", reply_markup=await main_buttons(list(await rep.get_api_names(message.from_user.id))))








        

    

# @fsmRouter.callback_query_handler(lambda c: c.data.startswith('button_'))
# async def process_button(callback_query: CallbackQuery):
#     data = callback_query.data.split('_')
#     index = int(data[1])  # Индекс кнопки
#     text = data[2]         # Текст кнопки

#     await callback_query.answer(f'Вы нажали кнопку: {text} с индексом: {index}')


    
    
    



    
        
    

    

    







