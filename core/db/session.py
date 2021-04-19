from contextvars import ContextVar, Token
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from core.config import config

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_id() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


engine = create_engine(config.DB_URL, pool_recycle=3600)
session: Union[Session, scoped_session] = scoped_session(
    sessionmaker(autocommit=True, autoflush=False, bind=engine),
    scopefunc=get_session_id,
)
Base = declarative_base()
