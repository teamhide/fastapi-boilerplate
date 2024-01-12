from uuid import uuid4

import pytest

from core.db.session import set_session_context, reset_session_context
from tests.support.test_db_coordinator import TestDbCoordinator

test_db_coordinator = TestDbCoordinator()


@pytest.fixture(scope="function", autouse=True)
def session_context():
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    yield
    reset_session_context(context=context)


@pytest.fixture
def db():
    test_db_coordinator.apply_alembic()
    yield
    test_db_coordinator.truncate_all()
