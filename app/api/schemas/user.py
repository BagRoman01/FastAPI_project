from pydantic import BaseModel


# Pydantic schema for creating a new user
class UserCreate(BaseModel):
    username: str
    password: str
