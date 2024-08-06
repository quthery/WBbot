from aiogram import Router, F
from aiogram.types import Message
from app.database.repository import Repository as rep
from app.keyboards.ReplyKeyboard import main_buttons
from app.keyboards.InlineKeyboard import cancel_buttons
import aiohttp
import asyncio


router = Router()



@router.message(F.text == "FAQ📖")
async def FAQ(message: Message):
    await message.answer("Часто задаваемые вопросы:\nhttps://telegra.ph/FAQ-WBcheckerBot-08-03", reply_markup=await main_buttons(list(await rep.get_api_names(message.from_user.id))))


@router.message(F.text == "Начать ожидание заказов⌚")
async def wait_for_order(message: Message):
    url = "https://marketplace-api.wildberries.ru/api/v3/orders/new"
    
    async with aiohttp.ClientSession() as session:
        tokens = await rep.get_api_keys(message.from_user.id)
        while True:
            for token in tokens:
                print(token)
                async with session.get(url, headers={"Authorization": token}) as response:
                    if response.status == 200:
                        data = await response.json()
                        orders = data.get("orders", [])
                        articles = await rep.get_articles(token)
                        for order in orders:
                            article = order.get("article")
                            print(article)
                            if article in articles:
                                await message.answer(f"НА АРТИКУЛ {article} ПРИШЕЛ ЗАКАЗ СОБЕРИТЕ ЕГО И УБЕРИТЕ 1 ПОЗИЦИЮ С ОСТАТКА")
            await asyncio.sleep(100)#это задержка 100 секунд








        

    

# @fsmRouter.callback_query_handler(lambda c: c.data.startswith('button_'))
# async def process_button(callback_query: CallbackQuery):
#     data = callback_query.data.split('_')
#     index = int(data[1])  # Индекс кнопки
#     text = data[2]         # Текст кнопки

#     await callback_query.answer(f'Вы нажали кнопку: {text} с индексом: {index}')


    
    
    



    
        
    

    

    







