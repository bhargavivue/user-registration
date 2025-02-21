from pydantic import BaseModel, Field, EmailStr

from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class UserCreate(BaseModel):
    user_id: int
    user_name: str
    userfirst_name: str
    userlast_name:str
    password:str
    conform_password:str
    mobile_number: str
    email:EmailStr
    #gender:str
class UserLogin(BaseModel):
    user_id: int
    password: str
    
class UserResponse(BaseModel):
    user_id: int
    user_name: str
    userfirst_name: str
    userlast_name:str
    mobile_number: str
    email:EmailStr
    gender:str