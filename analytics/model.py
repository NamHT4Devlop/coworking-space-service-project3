from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, TIMESTAMP

class BaseMixin:
    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class Token(BaseMixin, Base):
    __tablename__ = 'tokens'

    user_id = Column(Integer, nullable=False)
    token = Column(String(6), nullable=False)
    used_at = Column(TIMESTAMP, nullable=True)

    def __repr__(self):
        return (f"<Token(id={self.id}, user_id={self.user_id}, "
                f"token='{self.token}', created_at='{self.created_at}', "
                f"used_at='{self.used_at}')>")
