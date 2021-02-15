# FastAPI Boilerplate

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

Custom user class automatically decoded header token and store user information into `request.user`

If you want to modify custom user class, you have to update below files.

1. core/fastapi/schemas/current_user.py
2. core/fastapi/middlewares/authentication.py

### CurrentUser

```python
class CurrentUser(BaseModel):
    id: int = None
```
Just add more fields that you need.

### AuthBackend

```python
current_user = CurrentUser()
```

After line 18, assign values that you added on `CurrentUser`.