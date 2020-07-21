from starter.db_session import Base, engine, db_session

from Client import Client
from Item import Item
from orders import Order
from Vehicle import Vehicle
from orders.OrderStatus import OrderStatus

Base.metadata.drop_all(engine, checkfirst=True)
Base.metadata.create_all(engine, checkfirst=True)

##Create starting registries
to_add = []
for i in ["Created","Scheduled for delivery", "Delivered", "Canceled"]:
    to_add.append(OrderStatus(order_status_name=i))

db_session.add_all(to_add)
db_session.commit()