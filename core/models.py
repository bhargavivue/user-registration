from sqlalchemy import Column, Integer, String, DateTime
from core.database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)
    age = Column(Integer)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
