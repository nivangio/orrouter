from starter import BaseMixin, Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float
from sqlalchemy.orm import relationship
from orders import Order

class Client(Base, BaseMixin):
    __tablename__ = "CLIENTS"

    company_name = Column(String)
    contact_name = Column(String)
    address = Column(String)
    lat = Column(Float)
    long = Column(Float)

    orders = relationship(Order, backref="client")
