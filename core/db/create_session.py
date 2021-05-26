from uuid import uuid4

from .session import session, set_session_context, reset_session_context


def create_session(func):
    async def _create_session(*args, **kwargs):
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            await func(*args, **kwargs)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.remove()
            reset_session_context(context=context)

    return _create_session
