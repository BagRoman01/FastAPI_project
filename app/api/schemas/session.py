from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict


class SessionCreate(BaseModel):
    user_id: int
    refresh_token: str
    fingerprint: str
    exp_at: datetime
    created_at: datetime = datetime.now(timezone.utc)


class Session(SessionCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
