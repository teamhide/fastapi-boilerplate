# FastAPI Boilerplate

# Features
- SQlAlchemy session
- Custom user class
- Top-level dependency
- Dependencies for specific permissions

## SQLAlchemy for asyncio context

```python
from core.db import session
```
Just import session and use it.


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

1. core/fastapi/schemas/current_user.py
2. core/fastapi/middlewares/authentication.py

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

Set a callable function when initialize FastAPI() app through `dependencies` argument.

## Dependencies for specific permissions

There is 2 permissions `IsAdmin` and `IsAuthenticated`.

`IsAdmin` check current user is admin or not.

`IsAuthenticated` check current user is authenticated.
 
```python

```
