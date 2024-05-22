from logyca_postgres.utils.helpers.functions import html_escaping_special_characters
from logyca_postgres.utils.helpers.singleton import Singleton
from sqlalchemy import text as text_to_sql
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, DeclarativeMeta
from starlette.exceptions import HTTPException
from starlette.status import HTTP_409_CONFLICT
from typing import AsyncGenerator

AsyncDeclarativeBaseORM: DeclarativeMeta = declarative_base()

class AsyncConnEngine(metaclass=Singleton):
    """Description
    FastAPI
    ```python
    from fastapi import FastAPI, Depends, HTTPException
    from logyca_postgres import AsyncConnEngine, commit_rollback_async, check_connection_async
    from sqlalchemy import text as text_to_sql
    from sqlalchemy.ext.asyncio import AsyncSession
    import os

    DB_USER=os.getenv('DB_USER','postgres')
    DB_PASS=os.getenv('DB_PASS','xxx')
    DB_HOST=os.getenv('DB_HOST','localhost')
    DB_PORT=os.getenv('DB_PORT',5432)
    DB_NAME=os.getenv('DB_NAME','test')
    ssl_enable_like_local_docker_container=False

    app = FastAPI()

    conn_async_session=AsyncConnEngine(
        url_connection=AsyncConnEngine.build_url_connection(user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT,database=DB_NAME,ssl_enable=ssl_enable_like_local_docker_container),
        server_settings=AsyncConnEngine.server_settings(pool_size=5,max_overflow=1,pool_recycle=10800,application_name="MyApp - AsyncConnEngine")
        )

    '''
    The connection pool (pool_size) after the first query will remain open until the application is stopped.
    '''

    @app.get("/simulated_query_async/")
    async def read_item(async_session:AsyncSession = Depends(conn_async_session)):
        try:
            status, date_time_check_conn = await check_connection_async(async_session)
            if(status):
                query = text_to_sql("SELECT now();")
                result = await async_session.execute(query)
                simulated_query = result.scalar_one_or_none()
                await commit_rollback_async(async_session)
                return {"date_time_check_conn": date_time_check_conn, "simulated_query": simulated_query}
            else:
                raise HTTPException(status_code=404, detail="async_session connect db error...")
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"error: {e}")
    ```
    Worker or script
    ```python
    from logyca_postgres import AsyncConnEngine, commit_rollback_async, check_connection_async
    from sqlalchemy import text as text_to_sql
    from sqlalchemy.ext.asyncio import AsyncSession
    import asyncio
    import os

    DB_USER=os.getenv('DB_USER','postgres')
    DB_PASS=os.getenv('DB_PASS','xxx')
    DB_HOST=os.getenv('DB_HOST','localhost')
    DB_PORT=os.getenv('DB_PORT',5432)
    DB_NAME=os.getenv('DB_NAME','test')
    ssl_enable_like_local_docker_container=False

    conn_async_session=AsyncConnEngine(
        url_connection=AsyncConnEngine.build_url_connection(user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT,database=DB_NAME,ssl_enable=ssl_enable_like_local_docker_container),
        server_settings=AsyncConnEngine.server_settings(pool_size=5,max_overflow=1,pool_recycle=10800,application_name="MyApp - AsyncConnEngine")
                )

    '''
    The connection pool (pool_size) after the first query will remain open until the application is stopped or the engine is terminated: close_engine().
    '''

    async def methods(async_session:AsyncSession):
        status, date_time_check_conn = await check_connection_async(async_session)
        if(status):
            query = text_to_sql("SELECT now();")
            result = await async_session.execute(query)
            simulated_query = result.scalar_one_or_none()
            await commit_rollback_async(async_session)
            print(f"date_time_check_conn={date_time_check_conn},simulated_query={simulated_query}")
        else:
            print("async_session connect db error...")
    async def main():
        async for async_session in conn_async_session.get_async_session():
            await methods(async_session)
        await conn_async_session.close_engine()

    if __name__ == "__main__":
        asyncio.run(main())
    ```
    # Example of concepts that use a library with a singleton pattern and connection to multiple engines with yield dependency injection

    The library uses a singleton pattern "class SyncConnEngine(metaclass=Singleton):", where the class is allowed to be instantiated only once. You can create another connection to another engine but you must create an inherited class in order to create a new configuration instance.

    Example:
    class AsyncConnEngine(SyncConnEngine):
        def __init__(self, url_connection,server_settings):
            super().__init__(url_connection,server_settings)
    async_session_x=AsyncConnEngineX(
        url_connection=SyncConnEngine.build_url_connection(user=settings.DB_USER_X,password=settings.DB_PASS_X,host=settings.DB_HOST_X,port=settings.DB_PORT_X,database=settings.DB_NAME_X,ssl_enable=settings.DB_SSL_X),
        server_settings=SyncConnEngine.server_settings(pool_size=5,max_overflow=1,pool_recycle=10800,application_name=f"{App.Settings.NAME} - SyncConnEngineX")
        )

    """
    def __init__(self,url_connection:str,server_settings:dict):
        self.url_connection=url_connection
        self.__engine = create_async_engine(
            url=url_connection,
            future=True,
            echo=False,
            pool_size=server_settings["pool_size"],
            max_overflow=server_settings["max_overflow"],
            pool_recycle=server_settings["pool_recycle"],
            connect_args={
                "server_settings": {"application_name": server_settings["application_name"]}
            }
        )
        self.__async_session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=self.__engine, class_=AsyncSession) 

    async def __call__(self):
        '''Description
        Used by fastapi dependency injection
        '''
        async with self.__async_session_maker() as async_sessionmaker:
            yield async_sessionmaker

    async def get_async_session(self)->AsyncGenerator[AsyncSession, None]:
        '''Description
        Used by console scripts
        '''
        async with self.__async_session_maker() as async_sessionmaker:
            yield async_sessionmaker

    async def close_engine(self):
        await self.__engine.dispose()

    @classmethod
    def server_settings(self,pool_size:int, max_overflow:int, pool_recycle:int, application_name:str) -> None:
        """Descriptions

        Args:
            pool_size (int): Postgres server or engine configuration parameter given in seconds.
                             Is the maximum number of connections that an application can keep open simultaneously
            max_overflow (int): Postgres server or engine configuration parameter given in seconds.
                             Determines the maximum number of additional connections that can be temporarily created when demand exceeds the maximum connection pool size.
            pool_recycle (int): Postgres server or engine configuration parameter given in seconds.
                             Specifies the time after which connections in the pool are automatically recycled to avoid connection stagnation or blocking issues.
            application_name (str): Postgres server or engine configuration parameter given in text.
                             Seconds: Description that can be seen when listing the connected user sessions in the database.
        """
        return {
            "pool_size": pool_size,
            "max_overflow": max_overflow,
            "pool_recycle": pool_recycle,
            "application_name": application_name
        } 
    
    @classmethod
    def build_url_connection(cls,user:str,password:str,host:str,port:int,database:str,ssl_enable:bool):
        """Descriptions
        Data for connection to the database
            Args:
                ssl_enable (str): whether ssl=require is needed or not
        """
        dialect="postgresql"
        driver="asyncpg"
        ssl_option = '?ssl=require' if ssl_enable else ''
        ps_escaping_special_characters=html_escaping_special_characters(password)
        return f"{dialect}+{driver}://{user}:{ps_escaping_special_characters}@{host}:{port}/{database}{ssl_option}"

async def check_connection_async(async_session: AsyncSession)->tuple[bool,str]:
    '''Description
    :return tuple[bool,str]: status, date_time now'''    
    try:
        query = text_to_sql(f"SELECT now();")
        result:CursorResult = await async_session.execute(query)
        date_time = result.scalar_one_or_none()
        if date_time is not None:
            return True, date_time
        else:
           return False, ''
    except Exception as e:
        return False, str

async def commit_rollback_async(async_session: AsyncSession):
    try:
        await async_session.commit()
    except IntegrityError as integrity_exc:
        await async_session.rollback()
        msg_error_already_exists = "The record you are trying to create already exists."
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=msg_error_already_exists,
        )
    except Exception as exc:
        await async_session.rollback()
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=f"{exc}",
        )

