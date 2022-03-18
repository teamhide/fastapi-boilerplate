from asyncio import current_task
from typing import Union

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from core.config import config

engine = create_async_engine(config.DB_URL, pool_recycle=3600)
async_session_factory = sessionmaker(bind=engine, class_=AsyncSession)
session: Union[Session, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=current_task,
)
Base = declarative_base()
