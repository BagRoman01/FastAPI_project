from pydantic import BaseModel, ConfigDict


# Pydantic schema for creating a new user
class UserCreate(BaseModel):
    age: int
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserFromDb(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    age: int

