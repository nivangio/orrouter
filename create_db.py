from starter.db_session import Base, engine, db_session

from user import User
from orders.OrderStatus import OrderStatus
from Client import Client
from Item import Item
from orders import Order
from Vehicle import Vehicle
from routes.Route import RouteVehicle, Route

Base.metadata.drop_all(engine, checkfirst=True)
Base.metadata.create_all(engine, checkfirst=True)

##Create starting registries
to_add = []
for i in ["Created","Scheduled for delivery", "Delivered", "Canceled"]:
    to_add.append(OrderStatus(order_status_name=i))

db_session.add_all(to_add)
db_session.commit()

User.create(username = "test", password="abcd")