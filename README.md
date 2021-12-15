# FastAPI Boilerplate

# Features
- SQLAlchemy session
- Custom user class
- Top-level dependency
- Dependencies for specific permissions
- Celery
- Dockerize(Hot reload)
- Event Publisher

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

## Event Publisher

First, you have to make your own event through inherit `BaseEvent`.

```python
from core.event.base_event import BaseEvent
from core.event.slack.parameter import SlackEventParameter


class SlackEvent(BaseEvent):
    async def run(self, parameter: SlackEventParameter) -> None:
        print(f"SLACK EVENT / {parameter.channel} / {parameter.message}")
```

(Optional) If you want to use parameter, make parameter class.

```python
from pydantic import BaseModel


class SlackEventParameter(BaseModel):
    channel: str
    message: str
```

Add `@EventListener()` decorator to your method that will publish event.
```python
from core.event.slack import SlackEvent
from core.event import EventListener


@EventListener()
async def test():
    pass
```

Store event via `EventHandler` class.

```python
from core.event import get_event_handler
from core.event.slack import SlackEvent, SlackEventParameter


@EventListener()
async def test():
    event_handler = get_event_handler()
    await event_handler.store(
        event=SlackEvent,
        parameter=SlackEventParameter(channel="channel", message="message"),
    )
```

Then, `@EventListener` automatically publish event.

In case of use with `@Transactional`, you have to used in the outermost.

```python
@EventListener()  # HERE
@Transactional()
async def test():
    ...
```