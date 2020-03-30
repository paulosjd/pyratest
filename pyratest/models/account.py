from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import relation

from .meta import Base


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    name = Column(Unicode(40), nullable=False)
    orders = relation('Order', backref='account')
