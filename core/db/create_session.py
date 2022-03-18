from .session import session


def create_session(func):
    async def _create_session(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.remove()

    return _create_session
