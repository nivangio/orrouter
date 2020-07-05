from starter import Searchable, Base
from sqlalchemy import Column, String

class OrderStatus(Base, Searchable):
    __tablename__ = 'ORDER_STATUSES'

    order_status_name = Column(String)