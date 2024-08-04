from app.database.models import Users, Api
from app.database.init import new_session
from sqlalchemy.future import select
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
            


