from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from core.schemas import UserCreate, UserLogin, GenderEnum, UserResponse
from datetime import timedelta, datetime
from repositories.user_repository import UserRepository
from core.utils import hash_password, validate_password, verify_password
from core.models import User, LoginAttempt  # Ensure LoginAttempt model is imported

LOCKOUT_ATTEMPTS = 3
LOCKOUT_DURATION = timedelta(minutes=15)

class UserService:
    @staticmethod
    def register_user(db: Session, user_data: UserCreate, gender: GenderEnum):
        """Handles user registration logic."""
        # Validate password
        if not validate_password(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least 8 characters, including uppercase, lowercase, number, and special character."
            )

        # Check if username already exists
        if UserRepository.get_user_by_user_id(db, user_data.user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists."
            )

        # Hash password and create user
        hashed_password = hash_password(user_data.password)
        user = User(
            user_id=user_data.user_id,
            user_name=user_data.user_name,
            userfirst_name=user_data.userfirst_name,
            userlast_name=user_data.userlast_name,
            password=hashed_password,
            email=user_data.email,
            mobile_number=user_data.mobile_number,
            gender=gender
        )
        return UserRepository.create_user(db, user)

    @staticmethod
    def login_user(db: Session, login_data: UserLogin):
        """Handles user login logic."""
        user = UserRepository.get_user_by_user_id(db, login_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials."
            )

        # Fetch login attempt record or create a new one
        attempt = UserRepository.get_login_attempts_by_user_id(db, login_data.user_id)
        if not attempt:
            attempt = LoginAttempt(user_id=user.user_id, attempts=0, is_locked=False, locked_at=None)
            db.add(attempt)
            db.commit()
            db.refresh(attempt)

        
        if attempt.is_locked and attempt.locked_at:
            lock_expiry = attempt.locked_at + LOCKOUT_DURATION
            if datetime.utcnow() < lock_expiry:
                raise HTTPException(status_code=403, detail="Account is locked. Try again later.")
            else:
                # Unlock user if lock duration has expired
                attempt.is_locked = False
                attempt.attempts = 0
                attempt.locked_at = None
                db.commit()

        # Verify password
        if not verify_password(login_data.password, user.password):
            attempt.attempts += 1  # Increase attempt count
            db.commit()
            db.refresh(attempt)
            if attempt.attempts >= LOCKOUT_ATTEMPTS:
                attempt.is_locked = True
                attempt.locked_at = datetime.utcnow()
                db.commit()
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Account locked due to too many failed login attempts."
                )

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
        else:
            # Reset failed attempts on successful login
            attempt.is_locked = False
            attempt.attempts = 0
            attempt.locked_at = None
            db.commit()
            db.refresh(attempt)
        return  UserResponse(
            user_id=user.user_id,
            user_name=user.user_name,
            userfirst_name=user.userfirst_name,
            userlast_name=user.userlast_name,
            email=user.email,
            mobile_number=user.mobile_number,
            gender=user.gender
        )
   def change passw