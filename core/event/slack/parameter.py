from pydantic import BaseModel


class SlackEventParameter(BaseModel):
    channel: str
    message: str
