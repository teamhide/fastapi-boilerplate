# FastAPI Boilerplate

# Features
- SQLAlchemy session
- Custom user class
- Top-level dependency
- Dependencies for specific permissions
- Celery
- Dockerize(Hot reload)
- Event dispatcher
- Cache

## SQLAlchemy for asyncio context

### Session
```python
from core.db import session
```
Just import session and use it.

### Transaction

To guarantee of transaction, session's `autocommit` option is `True`.

So you have to use `Transaction` class.

```python
from core.db import Transaction, session


@Transaction()
async def create_user(self):
    session.add(User(email="padocon@naver.com"))
```
Usage as decorator.
```python
from core.db import Transaction, session


with Transaction():
    session.add(User(email="padocon@naver.com"))
```
Usage as context manager.

In this case, only one transaction is supported.

**Note. Do not use explicit `commit()`. `Transaction` class automatically do.**

### Standalone session

According to the current settings, the session is set through middleware.

However, it doesn't go through middleware in tests or background tasks.

So you need to use the `@create_session` decorator.

```python
from core.db import create_session


@create_session
def test_something():
    ...
```

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
    id: int = None
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

Permissions `IsAdmin` and `IsAuthenticated` have already been implemented.
 
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
async def get_user_list(limit: int = 10, prev: int = None):
    pass
```
Insert permission through `dependencies` argument.

If you want to make your own permission, inherit `BasePermission` and implement `has_permission()` function.

## Event dispatcher

Refer the README of https://github.com/teamhide/fastapi-event

## Cache

```python
from core.helpers.cache import Cacheable


@Cacheable(prefix="get_user", ttl=60)
async def get_user():
    ...
```

Use the `Cacheable` decorator to cache the return value of a function.

Depending on the argument of the function, caching is stored with a different value through internal processing.
