from starter import BaseMixin, Base
from sqlalchemy import Column, String, Numeric

class Vehicle(Base, BaseMixin):
    __tablename__ = "VEHICLES"

    vehicle_name = Column(String)
    plate = Column(String)
    capacity = Column(Numeric)
