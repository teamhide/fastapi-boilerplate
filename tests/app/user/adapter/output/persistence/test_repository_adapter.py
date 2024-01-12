import pytest

from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter

repository_adapter = UserRepositoryAdapter()


@pytest.mark.asyncio
async def test_get_users(db):
    pass
