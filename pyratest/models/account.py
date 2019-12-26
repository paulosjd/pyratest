from sqlalchemy import (
    Column, Index, Integer, Unicode,
)

from .meta import Base


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    name = Column(Unicode(40), nullable=False)