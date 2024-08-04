import aiohttp
import asyncio
from datetime import datetime, timedelta

async def fetch_sales(api_key):
    # Устанавливаем дату начала (30 дней назад)
    date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S%z')
    
    url = "https://statistics-api.wildberries.ru/api/v1/supplier/sales"
    headers = {
        "Authorization": api_key
    }
    params = {
        "dateFrom": date_from,
        "flag": 0  # Получаем данные с последними изменениями
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                print(data)
                return data
            else:
                return {"error": f"Ошибка {response.status}: {await response.text()}"}

# Пример использования
api_key = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwODAxdjEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTczODQ3MTAyNywiaWQiOiJkZjY3MzA0Ni0yMDc3LTQyMjktYTkxMy0xMTVhZWY1ZTU1ZTYiLCJpaWQiOjExNjg3MTk0LCJvaWQiOjI3MTY2OCwicyI6MTQwNiwic2lkIjoiMjM2MzBmZmMtODE1MC00NWIyLWE1NjktYTI3YzFkMTlhZjUwIiwidCI6ZmFsc2UsInVpZCI6MTE2ODcxOTR9.cA-tP38mQCTLqUWKyfS4jXSIs-GVtkYrdwpZ0uN-jWe7NAH6nqMXNTY1tywKP81dY1eK6s5hQr4Xzm3sRKl-xg"  # Замените на ваш API ключ
asyncio.run(fetch_sales(api_key))
