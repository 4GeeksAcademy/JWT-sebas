from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __init__(self, email: str, password: str, username: str):
       

        self.email = (email or "").strip().lower()
        self.username = (username or "").strip()
        self.set_password(password)

    
    def _set_password_hash(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def set_password(self, password: str) -> None:
        if not password:
            raise ValueError("Password requerido")
        self._set_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    
    def serialize(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active
        }

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"
