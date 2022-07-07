from pydantic import BaseModel


class SynchronizeSessionEnum(BaseModel):
    FETCH = "fetch"
    EVALUATE = "evaluate"
    FALSE = False
