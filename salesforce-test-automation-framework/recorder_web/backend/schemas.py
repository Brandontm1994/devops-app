from pydantic import BaseModel

class RecorderEvent(BaseModel):
    action: str
    locator: dict
    value: str | None = None
    timestamp: float
