from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from core.config import get_config

engine = create_engine(get_config().DB_URL)
session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
)
Base = declarative_base()
