from starter.db_session import Base, engine

from Client import Client
from Item import Item
from orders import Order
from Vehicle import Vehicle

Base.metadata.drop_all(engine, checkfirst=True)
Base.metadata.create_all(engine, checkfirst=True)
