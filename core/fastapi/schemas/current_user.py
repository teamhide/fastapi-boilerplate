from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: int = None

    class Config:
        validate_assignment = True
