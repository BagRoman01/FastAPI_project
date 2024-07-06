from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SessionCreate(BaseModel):
    user_id: int
    refresh_token: str
    fingerprint: str
    exp_at: float
    created_at: float = datetime.now()


class Session(SessionCreate):
    session_id: int
    model_config = ConfigDict(from_attributes=True)
