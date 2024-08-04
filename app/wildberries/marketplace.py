import aiohttp
import asyncio

token = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwODAxdjEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTczODQ3MTAyNywiaWQiOiJkZjY3MzA0Ni0yMDc3LTQyMjktYTkxMy0xMTVhZWY1ZTU1ZTYiLCJpaWQiOjExNjg3MTk0LCJvaWQiOjI3MTY2OCwicyI6MTQwNiwic2lkIjoiMjM2MzBmZmMtODE1MC00NWIyLWE1NjktYTI3YzFkMTlhZjUwIiwidCI6ZmFsc2UsInVpZCI6MTE2ODcxOTR9.cA-tP38mQCTLqUWKyfS4jXSIs-GVtkYrdwpZ0uN-jWe7NAH6nqMXNTY1tywKP81dY1eK6s5hQr4Xzm3sRKl-xg"

async def fetch_new_orders(token: str):
    url = "https://marketplace-api.wildberries.ru/api/v3/orders/new"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                print("Успешный запрос:", data)
                return data
            else:
                print("Ошибка:", response.status, await response.text())
                return response.status



