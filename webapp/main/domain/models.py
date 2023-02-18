from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

from webapp.main.infra.persistence.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Integer)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return "<User(id='%s', email='%s', \
                hashed_password='%s', \
                is_active='%s')>" % (
            self.id, self.email, self.hashed_password, self.is_active)
