from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from core.schemas import UserCreate, UserLogin
from repositories.user_repository import UserRepository
from core.utils import hash_password, validate_password, verify_password
from core.models import User

class UserService:
    @staticmethod
    def register_user(db: Session, user_data: UserCreate):
        """Handles user registration logic."""
        # Validate password
        if not validate_password(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least 8 characters, including uppercase, lowercase, number, and special character."
            )

        # Check if username already exists
        if UserRepository.get_user_by_username(db, user_data.user_name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists."
            )

        # Hash password and create user
        hashed_password = hash_password(user_data.password)
        user = User(
            user_name=user_data.user_name,
            password=hashed_password,
            full_name=user_data.full_name,
            age=user_data.age,
        )
        return UserRepository.create_user(db, user)

    @staticmethod
    def login_user(db: Session, login_data: UserLogin):
        """Handles user login logic."""
        user = UserRepository.get_user_by_username(db, login_data.user_name)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        if not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password."
            )
        return {"message": "Login successful!"}
