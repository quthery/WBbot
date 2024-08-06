from app.database.models import Users, Api, Article, OrderUID
from app.database.init import new_session
from sqlalchemy.future import select
from sqlalchemy import update
import asyncio


class Repository:
    @classmethod
    async def add_user(cls, id: int, full_name: str, username: str, password: str) -> int:
        async with new_session() as session:
            user = Users(id=id, fullname=full_name, username=username, password=password)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id
        
    @classmethod
    async def add_api(cls, user_id: int, api_key: str, api_name: str) -> int:
        async with new_session() as session:
            api = Api(user_id=user_id, api_key=api_key, name=api_name)
            session.add(api)
            await session.flush()
            await session.commit()
            return api.id
        
    @classmethod
    async def add_article(cls, token:str, art: str, quantity: int, days: int = 0) -> None:
        async with new_session() as session:
            item = Article(api_key=token, art=art, quantity=quantity, days=days)
            session.add(item)
            await session.flush()
            await session.commit()
    @classmethod
    async def delete_article(cls, art: str) -> bool:
        async with new_session() as session:
            item = await session.execute(select(Article).where(Article.art == art))
            article = item.scalars().first()

            if article:
                await session.delete(article)
                await session.commit()
                return True
            return False

        
    @classmethod
    async def add_article_to_sklad(cls, art: str) -> None:
        async with new_session() as session:
            query = update(Article).where(Article.art == art).values(quantity=Article.quantity + 1)
            await session.execute(query)
            await session.commit()
    @classmethod
    async def minus_article_to_sklad(cls, art: str, count: int, token: str) -> int:
        async with new_session() as session:
            # Execute the query to check the quantity
            for_check = select(Article.quantity).where(Article.art == art, Article.api_key == token)
            for_check_result = await session.execute(for_check)
            quantity = for_check_result.scalar_one_or_none()

            # Check if the article exists
            if quantity is None:
                return 404  # Article not found

            # Update the quantity
            new_quantity = quantity - count
            if new_quantity <= 0:
                await cls.delete_article(art)
                return 400 # Indicate insufficient quantity

            query = update(Article).where(Article.art == art).values(quantity=new_quantity)
            await session.execute(query)
            await session.commit()
            
            return 200  # Successfully updated


    @classmethod
    async def add_article_count(cls, token: str, art: str, count: int) -> None:
        async with new_session() as session:
            for_check = select(Article).where(Article.art == art)
            for_check_second = await session.execute(for_check)
            for_check_result = for_check_second.scalar_one_or_none()
            
            if for_check_result is None:
                await cls.add_article(token, art, count)
            else:
                current_quantity = for_check_result.quantity  # Fetch current quantity
                new_quantity = int(current_quantity) + int(count)  # Calculate new quantity
                
                query = update(Article).where(Article.art == art).values(quantity=new_quantity)
                await session.execute(query)  # Execute the update query
            
            await session.commit()

        
    @classmethod
    async def get_api_names(cls, user_id: int = None):
        async with new_session() as session:
            query = select(Api.name)
            query = query.where(Api.user_id == user_id)

            result = await session.execute(query)
            api_keys = result.scalars().all()
            api_key_strings = [str(key) for key in api_keys]
            return api_key_strings
        
    @classmethod
    async def get_user(cls, id) -> int:
        try:
            async with new_session() as session:
                user = await session.get(Users, id)
                print(str(user.id))
                return str(user.id)
        except AttributeError:
            return 0
    @classmethod
    async def get_user_password(cls, id) -> int:
        try:
            async with new_session() as session:
                user = await session.get(Users, id)
                return str(user.password)
        except AttributeError:
            return 0
        
    @classmethod
    async def get_api_key(cls, user_id: int = None, name: str = None) -> list[str]:
        async with new_session() as session:
            query = select(Api.api_key)
            query = query.where(Api.user_id == user_id, Api.name == name)

            result = await session.execute(query)
            api_keys = result.scalars().all()
            api_key_strings = [str(key) for key in api_keys]
            return api_key_strings
        
    @classmethod
    async def get_api_keys(cls, user_id: int = None, name: str = None) -> list[str]:
        async with new_session() as session:
            query = select(Api.api_key)
            query = query.where(Api.user_id == user_id)

            result = await session.execute(query)
            api_keys = result.scalars().all()
            api_key_strings = [str(key) for key in api_keys]
            return api_key_strings
        
        
    @classmethod
    async def get_articles(cls, api: str = None) -> list[str]:
        async with new_session() as session:
            query = select(Article.art)
            query = query.where(Article.api_key == api)

            result = await session.execute(query)
            api_keys = result.scalars().all()
            api_key_strings = [str(key) for key in api_keys]
            return api_key_strings
            
    @classmethod
    async def add_uid(cls, uid: str, article: str) -> None:
        async with new_session() as session:
            uid = OrderUID(uid=uid, article=article)
            session.add(uid)
            await session.flush()
            await session.commit()

    @classmethod
    async def get_uids(cls, uid: str = None) -> list[str]:
        async with new_session() as session:
            query = select(OrderUID.uid)
            query = query.where(OrderUID.uid == uid)

            result = await session.execute(query)
            api_keys = result.scalars().all()
            api_key_strings = [str(key) for key in api_keys]
            return api_key_strings



