from sqlalchemy import Column, Unicode, BigInteger

from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(Unicode(255), nullable=False)
    email = Column(Unicode(255), nullable=False, unique=True)
    nickname = Column(Unicode(255), nullable=False, unique=True)
