from sqlalchemy import Column, Integer, DECIMAL, Unicode

from .meta import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    price = Column(DECIMAL, nullable=False)
    number = Column(Unicode(40), nullable=False)
