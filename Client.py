from starter import BaseMixin, Base, HasAddress
from sqlalchemy import Column, String, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship
from orders import Order

class Client(Base, BaseMixin, HasAddress):
    __tablename__ = "CLIENTS"

    user_id = Column(Integer, ForeignKey('USERS.id'))
    company_name = Column(String)
    contact_name = Column(String)
    address = Column(JSON)

    orders = relationship(Order, backref="client")