from dataclasses import dataclass
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, TIMESTAMP

Base = declarative_base()

@dataclass
class Token(Base):
    __tablename__ = 'tokens'

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, nullable=False)
    token: str = Column(String(6), nullable=False)
    created_at: str = Column(TIMESTAMP, nullable=False, default=func.now())
    used_at: str = Column(TIMESTAMP, nullable=True)
