# FastAPI Boilerplate

# Features
- Async SQLAlchemy session
- Custom user class
- Top-level dependency
- Dependencies for specific permissions
- Celery
- Dockerize(Hot reload)
- Event dispatcher
- Cache

## Run

```python
python3 main.py --env local|dev|prod --debug
```

## SQLAlchemy for asyncio context

```python
from core.db import Transactional, session


@Transactional()
async def create_user(self):
    session.add(User(email="padocon@naver.com"))
```

Do not use explicit `commit()`. `Transactional` class automatically do.

### Standalone session

According to the current settings, the session is set through middleware.

However, it doesn't go through middleware in tests or background tasks.

So you need to use the `@standalone_session` decorator.

```python
from core.db import standalone_session


@standalone_session
def test_something():
    ...
```

### Multiple databases

Go to `core/config.py` and edit `WRITER_DB_URL` and `READER_DB_URL` in the config class.


If you need additional logic to use the database, refer to the `get_bind()` method of `RoutingClass`.

## Custom user for authentication

```python
from fastapi import Request


@home_router.get("/")
def home(request: Request):
    return request.user.id
```

**Note. you have to pass jwt token via header like `Authorization: Bearer 1234`**

Custom user class automatically decodes header token and store user information into `request.user`

If you want to modify custom user class, you have to update below files.

1. `core/fastapi/schemas/current_user.py`
2. `core/fastapi/middlewares/authentication.py`

### CurrentUser

```python
class CurrentUser(BaseModel):
    id: int = Field(None, description="ID")
```

Simply add more fields based on your needs.

### AuthBackend

```python
current_user = CurrentUser()
```

After line 18, assign values that you added on `CurrentUser`.

## Top-level dependency

**Note. Available from version 0.62 or higher.**

Set a callable function when initialize FastAPI() app through `dependencies` argument.

Refer `Logging` class inside of `core/fastapi/dependencies/logging.py` 

## Dependencies for specific permissions

Permissions `IsAdmin`, `IsAuthenticated`, `AllowAll` have already been implemented.
 
```python
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
)


user_router = APIRouter()


@user_router.get(
    "",
    response_model=List[GetUserListResponseSchema],
    response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],  # HERE
)
async def get_user_list(
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
):
    pass
```
Insert permission through `dependencies` argument.

If you want to make your own permission, inherit `BasePermission` and implement `has_permission()` function.

**Note. In order to use swagger's authorize function, you must put `PermissionDependency` as an argument of `dependencies`.**

## Event dispatcher

Refer the README of https://github.com/teamhide/fastapi-event

## Cache

### Caching by prefix
```python
from core.helpers.cache import Cache


@Cache.cached(prefix="get_user", ttl=60)
async def get_user():
    ...
```

### Caching by tag
```python
from core.helpers.cache import Cache, CacheTag


@Cache.cached(tag=CacheTag.GET_USER_LIST, ttl=60)
async def get_user():
    ...
```

Use the `Cache` decorator to cache the return value of a function.

Depending on the argument of the function, caching is stored with a different value through internal processing.

### Custom Key builder

```python
from core.helpers.cache.base import BaseKeyMaker


class CustomKeyMaker(BaseKeyMaker):
    async def make(self, function: Callable, prefix: str) -> str:
        ...
```

If you want to create a custom key, inherit the BaseKeyMaker class and implement the make() method.

### Custom Backend

```python
from core.helpers.cache.base import BaseBackend


class RedisBackend(BaseBackend):
    async def get(self, key: str) -> Any:
        ...

    async def set(self, response: Any, key: str, ttl: int = 60) -> None:
        ...

    async def delete_startswith(self, value: str) -> None:
        ...
```

If you want to create a custom key, inherit the BaseBackend class and implement the `get()`, `set()`, `delete_startswith()` method.

Pass your custom backend or keymaker as an argument to init. (`/app/server.py`)

```python
def init_cache() -> None:
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())
```

### Remove all cache by prefix/tag

```python
from core.helpers.cache import Cache, CacheTag


await Cache.remove_by_prefix(prefix="get_user_list")
await Cache.remove_by_tag(tag=CacheTag.GET_USER_LIST)
```