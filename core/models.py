from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, func, Boolean
from core.database import Base
from enum import Enum as PyEnum
from datetime import timedelta


class GenderEnum(str, PyEnum):
    male = "male"
    female = "female"
    other = "other"


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True)
    userfirst_name = Column(String, unique=True)
    userlast_name = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    mobile_number=Column(String)
    gender = Column(Enum(GenderEnum), nullable=False)
    
class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False)
    attempts = Column(Integer, default=0)
    last_attempt_at = Column(DateTime, default=func.now(), nullable=False)
    is_locked = Column(Boolean, default=False)
    locked_at = Column(DateTime, nullable=True)

class PasswordHistory(Base):
    __tablename__ = "password_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False)
    old_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
   
    