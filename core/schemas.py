from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    user_name: str
    password: str
    full_name: str
    age: int

class UserLogin(BaseModel):
    user_name: str
    password: str
