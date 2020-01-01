from sqlalchemy import Column, Integer, ForeignKey

from .meta import Base


class OrderItem(Base):
    __tablename__ = 'orderitems'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'),
                        nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'),
                      nullable=False)
