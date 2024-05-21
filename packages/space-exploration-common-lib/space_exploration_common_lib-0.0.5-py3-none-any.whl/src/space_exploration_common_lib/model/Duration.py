from pydantic import BaseModel


class Duration(BaseModel):
    days: int
    hours: int
    minutes: int
    seconds: int
