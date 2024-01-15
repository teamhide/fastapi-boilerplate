import asyncio
from uuid import uuid4

import pytest
import pytest_asyncio

from core.db.session import (
    set_session_context,
    reset_session_context,
    session as db_session,
)
from tests.support.test_db_coordinator import TestDbCoordinator

test_db_coordinator = TestDbCoordinator()


@pytest.fixture(scope="function", autouse=True)
def session_context():
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    yield
    reset_session_context(context=context)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def session():
    test_db_coordinator.apply_alembic()
    yield db_session
    await db_session.remove()
    test_db_coordinator.truncate_all()
