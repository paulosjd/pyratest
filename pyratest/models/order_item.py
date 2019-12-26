from sqlalchemy import (
    Column, Integer, ForeignKey
)

from .meta import Base


class OrderItem(Base):
    __tablename__ = 'orderitems'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, unique=True, nullable=False)
    product = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
