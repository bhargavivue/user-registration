from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.schemas import UserCreate, UserLogin, GenderEnum
from services.user_service import UserService 

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", status_code=201)
def register_user(user: UserCreate, GenderEnum:GenderEnum, db: Session = Depends(get_db)):
    """Endpoint to register a new user."""
    UserService.register_user(db, user,GenderEnum)
    return {"message": "User registered successfully!"}

@router.post("/login")
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    """Endpoint to log in an existing user."""
    return UserService.login_user(db, login_data)
