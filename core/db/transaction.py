from functools import wraps

from app.enums import BaseEnum
from core.db import session


class Propagation(BaseEnum):
    REQUIRED = "required"
    REQUIRES_NEW = "required_new"


class Transaction:
    def __init__(self, propagation: Propagation = Propagation.REQUIRED):
        self.propagation = propagation

    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            try:
                if self.propagation == Propagation.REQUIRED:
                    result = await self.run_required(
                        function=function, args=args, kwargs=kwargs,
                    )
                elif self.propagation == Propagation.REQUIRES_NEW:
                    result = await self.run_requires_new(
                        function=function, args=args, kwargs=kwargs,
                    )
                else:
                    result = await self.run_requires_new(
                        function=function, args=args, kwargs=kwargs,
                    )
            except Exception as e:
                session.rollback()
                raise e
            return result

        return decorator

    async def run_required(self, function, args, kwargs):
        is_transaction_active = session().is_active

        if not is_transaction_active:
            session.begin(subtransactions=True)

        result = await function(*args, **kwargs)
        if not is_transaction_active:
            session.commit()

        return result

    async def run_requires_new(self, function, args, kwargs):
        if not session().is_active:
            session.begin()

        result = await function(*args, **kwargs)
        session.commit()

        return result

    def __enter__(self):
        session.begin(subtransactions=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
