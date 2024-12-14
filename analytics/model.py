from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, TIMESTAMP

Base = declarative_base()

class Token(Base):
    __tablename__ = 'tokens'

    # Columns
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String(6), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    used_at = Column(TIMESTAMP)

    # Constructor
    def __init__(self, user_id, token, used_at=None):
        self.user_id = user_id
        self.token = token
        self.used_at = used_at

    # Representation method
    def __repr__(self):
        return (
            f"<Token(id={self.id}, user_id={self.user_id}, token='{self.token}', "
            f"created_at='{self.created_at}', used_at='{self.used_at}')>"
        )

    # To dictionary method
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "token": self.token,
            "created_at": self.created_at,
            "used_at": self.used_at
        }

    # Update token method
    def update_token(self, new_token):
        self.token = new_token
        self.created_at = func.now()  # Update creation timestamp

    # Mark as used method
    def mark_as_used(self, used_timestamp=None):
        self.used_at = used_timestamp or func.now()
