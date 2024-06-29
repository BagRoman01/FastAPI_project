from pydantic import BaseModel


# Pydantic schema for creating a new user
class UserCreate(BaseModel):
    age: int
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str