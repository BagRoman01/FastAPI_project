from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.exceptions.auth_exceptions import ShortPasswordError


class UserCreate(BaseModel):
    age: int = Field(..., gt=0, le=120, description="Age must be between 1 and 120")
    username: str
    password: str

    @field_validator('password')
    def password_length(cls, value):
        if len(value) < 5:
            raise ShortPasswordError
        return value


class UserLogin(BaseModel):
    username: str
    password: str


class UserFromDb(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    hashed_password: str

