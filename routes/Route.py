from starter import BaseMixin, Base
from sqlalchemy import Column, String, JSON, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from Vehicle import Vehicle
from datetime import datetime
from .create_route import create_route

class RouteVehicle(Base):
    __tablename__ = "ROUTE_VEHICLE"

    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey('ROUTES.id'))
    vehicle_id = Column(Integer, ForeignKey('VEHICLES.id'))

class Route(Base, BaseMixin):
    __tablename__ = "ROUTES"

    user_id = Column(Integer, ForeignKey('USERS.id'))
    route_name = Column(String)
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)
    route = Column(JSON)

    vehicles = relationship("Vehicle", secondary="ROUTE_VEHICLE")

    def __init__(self, **kwargs):
        self.user_id = kwargs["user_id"]
        self.route_name = kwargs["route_name"]
        self.start = datetime.strptime(kwargs["order_date"] + " " + kwargs["start"], "%Y-%m-%d %H:%M")
        self.end = datetime.strptime(kwargs["order_date"] + " " + kwargs["end"], "%Y-%m-%d %H:%M")
        self.vehicles = Vehicle.get_multiple_by_id(list(map(lambda x: x["id"], kwargs["vehicles"])))
        self.route = create_route(self.user_id, self.start, self.end, self.vehicles)
