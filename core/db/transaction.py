from functools import wraps

from core.db import session


class Transaction:
    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            try:
                session.begin()
                result = await function(*args, **kwargs)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            return result

        return decorator

    def __enter__(self):
        session.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
