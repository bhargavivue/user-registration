from sqlalchemy.orm import Session
from core.models import User

class UserRepository:
    @staticmethod
    def get_user_by_username(db: Session, user_name: str) -> User:
        """Fetch a user by username."""
        return db.query(User).filter(User.user_name == user_name).first()

    @staticmethod
    def create_user(db: Session, user: User) -> User:
        """Add a new user to the database."""
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
