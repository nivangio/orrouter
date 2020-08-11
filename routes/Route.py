from starter import BaseMixin, Base
from sqlalchemy import Column, String, JSON, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from Vehicle import Vehicle
from datetime import datetime

class RouteVehicle(Base):
    __tablename__ = "ROUTE_VEHICLE"

    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey('ROUTES.id'))
    vehicle_id = Column(Integer, ForeignKey('VEHICLES.id'))

class Route(Base, BaseMixin):
    __tablename__ = "ROUTES"

    user_id = Column(Integer, ForeignKey('USERS.id'))
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)
    route = Column(JSON)

    vehicles = relationship("VEHICLES", secondary="ROUTE_VEHICLE")

    def __init__(self, **kwargs):
        self.vehicles = Vehicle.get_multiple_by_id(list(map(lambda x: x["id"], kwargs["vehicles"])))
        self.start = datetime.strptime(kwargs["order_date"] + " " + kwargs["start"], "%Y-%m-%d %H:%M")
        self.end = datetime.strptime(kwargs["order_date"] + " " + kwargs["end"], "%Y-%m-%d %H:%M")
        self.client_id = kwargs["client_id"]
        self.route =
