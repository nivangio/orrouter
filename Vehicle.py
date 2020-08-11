from starter import BaseMixin, Base
from sqlalchemy import Column, String, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Vehicle(Base, BaseMixin):
    __tablename__ = "VEHICLES"

    user_id = Column(Integer, ForeignKey('USERS.id'))
    vehicle_name = Column(String)
    plate = Column(String)
    capacity = Column(Numeric)

    routes = relationship("ROUTES", secondary="ROUTE_VEHICLE")